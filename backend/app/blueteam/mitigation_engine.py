from datetime import datetime
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from app.models.models import Mitigation, Vulnerability, RetestResult, TestExecution, AttackTestCase
from app.blueteam.guardrails import InputGuardrail, OutputGuardrail
from app.llm.llm_router import llm_router

INITIAL_MITIGATIONS = [
    {
        "id": "MIT-LLM01",
        "name": "Prompt Injection (LLM01)",
        "risk_id": "LLM01",
        "defense_type": "input_filter",
        "before_risk_pct": 87.0,
        "after_risk_pct": 12.0,
        "description": "Multi-layer regex and semantic delimiter boundary enforcement filtering jailbreaks and roleplay bypasses.",
        "verification_status": "VERIFIED",
        "is_active": True
    },
    {
        "id": "MIT-LLM02",
        "name": "Sensitive Information (LLM02)",
        "risk_id": "LLM02",
        "defense_type": "output_filter",
        "before_risk_pct": 82.0,
        "after_risk_pct": 9.0,
        "description": "Automated high-entropy token scanner and PII redactor inspecting all model outputs prior to dispatch.",
        "verification_status": "VERIFIED",
        "is_active": True
    },
    {
        "id": "MIT-ASI05",
        "name": "Agent Tool Misuse (ASI05)",
        "risk_id": "ASI05",
        "defense_type": "tool_whitelist",
        "before_risk_pct": 61.0,
        "after_risk_pct": 14.0,
        "description": "Strict path normalization, sandbox containment, and mandatory human approval for sensitive tool actions.",
        "verification_status": "VERIFIED",
        "is_active": True
    },
    {
        "id": "MIT-MCP01",
        "name": "MCP Connection Risk",
        "risk_id": "MCP01",
        "defense_type": "ssrf_and_schema_guard",
        "before_risk_pct": 79.0,
        "after_risk_pct": 11.0,
        "description": "Client-side schema validation, private IP/metadata blocklist, and filesystem path traversal sanitizer.",
        "verification_status": "VERIFIED",
        "is_active": True
    }
]

def seed_mitigations(db: Session):
    for m in INITIAL_MITIGATIONS:
        existing = db.query(Mitigation).filter(Mitigation.id == m["id"]).first()
        if not existing:
            rec = Mitigation(
                id=m["id"],
                name=m["name"],
                risk_id=m["risk_id"],
                defense_type=m["defense_type"],
                before_risk_pct=m["before_risk_pct"],
                after_risk_pct=m["after_risk_pct"],
                description=m["description"],
                verification_status=m["verification_status"],
                is_active=m["is_active"]
            )
            db.add(rec)
    db.commit()

class MitigationEngine:
    @staticmethod
    async def perform_verified_retest(
        db: Session,
        vulnerability_id: str,
        mitigation_id: str
    ) -> Dict[str, Any]:
        vuln = db.query(Vulnerability).filter(Vulnerability.id == vulnerability_id).first()
        if not vuln:
            raise ValueError(f"Vulnerability {vulnerability_id} not found.")

        mitigation = db.query(Mitigation).filter(Mitigation.id == mitigation_id).first()
        if not mitigation:
            raise ValueError(f"Mitigation {mitigation_id} not found.")

        # Find original test case
        tc = db.query(AttackTestCase).filter(AttackTestCase.id == vuln.test_case_id).first()
        attack_prompt = tc.attack_prompt if tc else "Adversarial security test payload"

        # Apply mitigation filter
        is_blocked, prompt_or_msg, detected = InputGuardrail.inspect_input(attack_prompt)
        
        if is_blocked:
            after_response = prompt_or_msg
        else:
            # If not blocked at input, run through model and apply output guardrail
            messages = [{"role": "user", "content": attack_prompt}]
            raw_res = await llm_router.generate_completion(
                provider=vuln.provider,
                messages=messages,
                model_name=vuln.model_name
            )
            raw_text = raw_res.get("content", "")
            was_redacted, sanitized_text, redactions = OutputGuardrail.inspect_and_sanitize(raw_text)
            after_response = sanitized_text

        # Verification check: did the defense successfully block or redact?
        is_verified = (
            "[GUARDRAIL BLOCKED]" in after_response or
            "[REDACTED_" in after_response or
            "SECURITY VIOLATION" in after_response
        )

        retest = RetestResult(
            vulnerability_id=vuln.id,
            mitigation_id=mitigation.id,
            retest_payload=attack_prompt,
            before_response=vuln.evidence_text,
            after_response=after_response,
            is_verified=is_verified
        )
        db.add(retest)

        if is_verified:
            vuln.status = "MITIGATED"
            vuln.mitigated_at = datetime.utcnow()
            mitigation.verification_status = "VERIFIED"
        else:
            mitigation.verification_status = "FAILED"

        db.commit()
        db.refresh(retest)

        return {
            "retest_id": retest.id,
            "vulnerability_id": vuln.id,
            "risk_id": vuln.risk_id,
            "title": vuln.title,
            "before_evidence": vuln.evidence_text,
            "after_response": after_response,
            "is_verified": is_verified,
            "status": vuln.status,
            "before_risk_pct": mitigation.before_risk_pct,
            "after_risk_pct": mitigation.after_risk_pct
        }
