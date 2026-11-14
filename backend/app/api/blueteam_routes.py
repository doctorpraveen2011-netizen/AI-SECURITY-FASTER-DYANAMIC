from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.schemas import MitigationToggleRequest, RetestRequest
from app.models.models import Mitigation, Vulnerability, RetestResult
from app.blueteam.mitigation_engine import MitigationEngine

router = APIRouter(prefix="/blueteam", tags=["Blue Team Mitigations"])

@router.get("/mitigations")
def list_mitigations(db: Session = Depends(get_db)):
    mitigations = db.query(Mitigation).all()
    return [{
        "id": m.id,
        "name": m.name,
        "risk_id": m.risk_id,
        "defense_type": m.defense_type,
        "before_risk_pct": m.before_risk_pct,
        "after_risk_pct": m.after_risk_pct,
        "description": m.description,
        "verification_status": m.verification_status,
        "is_active": m.is_active
    } for m in mitigations]

@router.post("/toggle")
def toggle_mitigation(request: MitigationToggleRequest, db: Session = Depends(get_db)):
    m = db.query(Mitigation).filter(Mitigation.id == request.mitigation_id).first()
    if not m:
        raise HTTPException(status_code=404, detail="Mitigation not found")
    m.is_active = request.is_active
    db.commit()
    return {
        "id": m.id,
        "name": m.name,
        "is_active": m.is_active,
        "message": f"Mitigation '{m.name}' active status set to {m.is_active}."
    }

@router.post("/retest")
async def run_verified_retest(request: RetestRequest, db: Session = Depends(get_db)):
    try:
        res = await MitigationEngine.perform_verified_retest(
            db=db,
            vulnerability_id=request.vulnerability_id,
            mitigation_id=request.mitigation_id
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/before-after")
def get_before_after_analysis(db: Session = Depends(get_db)):
    retests = db.query(RetestResult).order_by(RetestResult.timestamp.desc()).limit(20).all()
    results = []
    for r in retests:
        vuln = db.query(Vulnerability).filter(Vulnerability.id == r.vulnerability_id).first()
        mit = db.query(Mitigation).filter(Mitigation.id == r.mitigation_id).first()
        results.append({
            "id": r.id,
            "vulnerability_title": vuln.title if vuln else "Vulnerability Retest",
            "risk_id": vuln.risk_id if vuln else "LLM01",
            "mitigation_name": mit.name if mit else "Defense Guardrail",
            "before_evidence": r.before_response,
            "after_evidence": r.after_response,
            "is_verified": r.is_verified,
            "timestamp": r.timestamp.isoformat()
        })
    return results
