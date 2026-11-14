from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app.database.session import get_db, SessionLocal
from app.schemas.schemas import CampaignRunRequest, SingleTestRunRequest
from app.redteam.campaign_runner import CampaignRunner
from app.redteam.test_cases import RED_TEAM_TEST_CASES
from app.redteam.taxonomy import ALL_RISKS
from app.models.models import AttackCampaign, TestExecution, Vulnerability, AttackTestCase

router = APIRouter(prefix="/redteam", tags=["Automated Red Team Engine"])

@router.get("/risks")
def list_risk_taxonomy():
    return list(ALL_RISKS.values())

@router.get("/test-cases")
def list_test_cases():
    return RED_TEAM_TEST_CASES

@router.post("/run-single")
async def run_single_test(
    request: SingleTestRunRequest,
    db: Session = Depends(get_db)
):
    try:
        res = await CampaignRunner.run_single_test(
            db=db,
            test_case_id=request.test_case_id,
            provider=request.provider,
            model_name=request.model_name
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/run-campaign")
async def run_campaign(
    request: CampaignRunRequest,
    db: Session = Depends(get_db)
):
    campaign = await CampaignRunner.run_full_campaign(
        db=db,
        campaign_name=request.name,
        target_provider=request.target_provider,
        risk_ids=request.risk_ids
    )
    return {
        "id": campaign.id,
        "name": campaign.name,
        "target_provider": campaign.target_provider,
        "status": campaign.status,
        "total_tests": campaign.total_tests,
        "completed_tests": campaign.completed_tests,
        "vulnerabilities_found": campaign.vulnerabilities_found,
        "message": f"Campaign concluded with {campaign.completed_tests} test runs across {request.target_provider}."
    }

@router.post("/campaigns/{campaign_id}/cancel")
def cancel_campaign(campaign_id: str):
    CampaignRunner.cancel_campaign(campaign_id)
    return {"message": f"Cancellation signal dispatched for campaign {campaign_id}."}

@router.get("/campaigns")
def list_campaigns(db: Session = Depends(get_db)):
    campaigns = db.query(AttackCampaign).order_by(AttackCampaign.created_at.desc()).all()
    return [{
        "id": c.id,
        "name": c.name,
        "target_provider": c.target_provider,
        "status": c.status,
        "total_tests": c.total_tests,
        "completed_tests": c.completed_tests,
        "vulnerabilities_found": c.vulnerabilities_found,
        "created_at": c.created_at.isoformat()
    } for c in campaigns]

@router.get("/executions")
def list_test_executions(limit: int = 50, db: Session = Depends(get_db)):
    execs = db.query(TestExecution).order_by(TestExecution.executed_at.desc()).limit(limit).all()
    return [{
        "id": e.id,
        "test_case_id": e.test_case_id,
        "provider": e.provider,
        "model_name": e.model_name,
        "result": e.result,
        "severity": e.severity,
        "prompt_payload": e.prompt_payload,
        "raw_response": e.raw_response,
        "observed_behavior": e.observed_behavior,
        "latency_ms": e.latency_ms,
        "executed_at": e.executed_at.isoformat()
    } for e in execs]
