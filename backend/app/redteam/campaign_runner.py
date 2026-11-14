import asyncio
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.models import AttackCampaign, AttackTestCase, TestExecution, Vulnerability
from app.redteam.test_cases import RED_TEAM_TEST_CASES
from app.redteam.evaluator import AttackEvaluator
from app.llm.llm_router import llm_router
from app.core.config import settings

class CampaignRunner:
    ACTIVE_CAMPAIGNS: Dict[str, bool] = {}

    @classmethod
    def cancel_campaign(cls, campaign_id: str):
        cls.ACTIVE_CAMPAIGNS[campaign_id] = False

    @classmethod
    async def run_single_test(
        cls,
        db: Session,
        test_case_id: str,
        provider: str = "claude",
        model_name: Optional[str] = None
    ) -> Dict[str, Any]:
        tc = next((t for t in RED_TEAM_TEST_CASES if t["id"] == test_case_id), None)
        if not tc:
            raise ValueError(f"Test case {test_case_id} not found.")

        target_model = model_name or (
            settings.DEFAULT_CLAUDE_MODEL if provider == "claude" else settings.DEFAULT_GEMINI_MODEL
        )

        messages = [{"role": "user", "content": tc["attack_prompt"]}]
        start_time = time.time()
        
        # Invoke LLM Router (calls official Claude or Gemini SDK)
        res = await llm_router.generate_completion(
            provider=provider,
            messages=messages,
            model_name=target_model,
            temperature=0.3
        )
        latency = (time.time() - start_time) * 1000
        raw_text = res.get("content", "")

        eval_result = AttackEvaluator.evaluate(tc, raw_text)

        execution = TestExecution(
            test_case_id=tc["id"],
            provider=provider,
            model_name=target_model,
            prompt_payload=tc["attack_prompt"],
            raw_response=raw_text,
            observed_behavior=eval_result["observed_behavior"],
            result=eval_result["result"],
            severity=eval_result["severity"],
            evidence=eval_result["evidence"],
            latency_ms=round(latency, 2)
        )
        db.add(execution)

        if eval_result["result"] == "VULNERABLE":
            vuln = Vulnerability(
                risk_id=tc["risk_id"],
                test_case_id=tc["id"],
                provider=provider,
                model_name=target_model,
                title=f"{tc['title']} ({provider.upper()})",
                severity=eval_result["severity"],
                status="OPEN",
                evidence_text=eval_result["evidence"].get("matched_sample", raw_text[:200])
            )
            db.add(vuln)

        db.commit()
        db.refresh(execution)

        return {
            "execution_id": execution.id,
            "test_case_id": tc["id"],
            "risk_id": tc["risk_id"],
            "provider": provider,
            "model_name": target_model,
            "result": execution.result,
            "severity": execution.severity,
            "observed_behavior": execution.observed_behavior,
            "raw_response": execution.raw_response,
            "latency_ms": execution.latency_ms,
            "executed_at": execution.executed_at.isoformat()
        }

    @classmethod
    async def run_full_campaign(
        cls,
        db: Session,
        campaign_name: str = "OWASP 2026 Red Team Full Campaign",
        target_provider: str = "both",
        risk_ids: Optional[List[str]] = None
    ) -> AttackCampaign:
        # Determine providers to test
        providers = ["claude", "gemini"] if target_provider == "both" else [target_provider]

        # Filter test cases
        cases = RED_TEAM_TEST_CASES
        if risk_ids:
            cases = [c for c in cases if c["risk_id"] in risk_ids]

        total_tests = len(cases) * len(providers)

        campaign = AttackCampaign(
            name=campaign_name,
            target_provider=target_provider,
            status="running",
            total_tests=total_tests,
            completed_tests=0,
            vulnerabilities_found=0
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)

        cls.ACTIVE_CAMPAIGNS[campaign.id] = True

        for p in providers:
            model = settings.DEFAULT_CLAUDE_MODEL if p == "claude" else settings.DEFAULT_GEMINI_MODEL
            for tc in cases:
                if not cls.ACTIVE_CAMPAIGNS.get(campaign.id, True):
                    campaign.status = "cancelled"
                    db.commit()
                    return campaign

                messages = [{"role": "user", "content": tc["attack_prompt"]}]
                start_time = time.time()
                res = await llm_router.generate_completion(
                    provider=p,
                    messages=messages,
                    model_name=model,
                    temperature=0.3
                )
                latency = (time.time() - start_time) * 1000
                raw_text = res.get("content", "")

                eval_result = AttackEvaluator.evaluate(tc, raw_text)

                execution = TestExecution(
                    campaign_id=campaign.id,
                    test_case_id=tc["id"],
                    provider=p,
                    model_name=model,
                    prompt_payload=tc["attack_prompt"],
                    raw_response=raw_text,
                    observed_behavior=eval_result["observed_behavior"],
                    result=eval_result["result"],
                    severity=eval_result["severity"],
                    evidence=eval_result["evidence"],
                    latency_ms=round(latency, 2)
                )
                db.add(execution)

                if eval_result["result"] == "VULNERABLE":
                    campaign.vulnerabilities_found += 1
                    vuln = Vulnerability(
                        risk_id=tc["risk_id"],
                        test_case_id=tc["id"],
                        provider=p,
                        model_name=model,
                        title=f"{tc['title']} ({p.upper()})",
                        severity=eval_result["severity"],
                        status="OPEN",
                        evidence_text=eval_result["evidence"].get("matched_sample", raw_text[:200])
                    )
                    db.add(vuln)

                campaign.completed_tests += 1
                db.commit()

        campaign.status = "completed"
        campaign.completed_at = datetime.utcnow()
        db.commit()
        db.refresh(campaign)
        return campaign
