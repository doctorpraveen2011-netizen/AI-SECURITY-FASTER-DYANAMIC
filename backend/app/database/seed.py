from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.models import (
    User, RiskCategory, AttackTestCase, AttackCampaign, TestExecution,
    Vulnerability, Mitigation, MCPConnection, MCPEvent, AuditLog
)
from app.redteam.test_cases import seed_attack_test_cases
from app.blueteam.mitigation_engine import seed_mitigations
from app.rag.synthetic_data import seed_synthetic_knowledge_base
from app.mcp.poc_runner import MCPPocRunner

def seed_all_data(db: Session):
    # 1. Knowledge Base
    seed_synthetic_knowledge_base(db)

    # 2. Risk Categories & Test Cases
    seed_attack_test_cases(db)

    # 3. Mitigations
    seed_mitigations(db)

    # 4. MCP Connection & initial blocked event
    MCPPocRunner.initialize_connection(db)

    # 5. Seed initial executions to populate the 48 total tests / 27 vulnerabilities / 24 mitigated metrics
    existing_tests = db.query(TestExecution).count()
    if existing_tests == 0:
        campaign = AttackCampaign(
            name="OWASP 2026 Baseline Security Audit",
            target_provider="both",
            status="completed",
            total_tests=48,
            completed_tests=48,
            vulnerabilities_found=27,
            completed_at=datetime.utcnow() - timedelta(hours=2)
        )
        db.add(campaign)
        db.commit()
        db.refresh(campaign)

        test_cases = db.query(AttackTestCase).all()
        # Seed 48 test executions across Claude & Gemini
        count = 0
        for p in ["claude", "gemini"]:
            model = "claude-3-5-sonnet-20241022" if p == "claude" else "gemini-1.5-flash"
            for tc in test_cases:
                if count >= 48:
                    break
                is_vuln = count < 27
                status_res = "VULNERABLE" if is_vuln else "SAFE"
                
                exec_item = TestExecution(
                    campaign_id=campaign.id,
                    test_case_id=tc.id,
                    provider=p,
                    model_name=model,
                    prompt_payload=tc.attack_prompt,
                    raw_response="Simulated baseline model audit trace.",
                    observed_behavior="Adversarial evaluation recorded during baseline audit.",
                    result=status_res,
                    severity=tc.severity,
                    latency_ms=134000.0,
                    executed_at=datetime.utcnow() - timedelta(minutes=count * 5)
                )
                db.add(exec_item)
                
                # Seed vulnerability
                if is_vuln:
                    is_mitigated = count < 24
                    v = Vulnerability(
                        risk_id=tc.risk_id,
                        test_case_id=tc.id,
                        provider=p,
                        model_name=model,
                        title=f"{tc.title} ({p.upper()})",
                        severity=tc.severity,
                        status="MITIGATED" if is_mitigated else "OPEN",
                        evidence_text=f"Vulnerability pattern detected in prompt evaluation: {tc.vulnerability_trigger_pattern}",
                        found_at=datetime.utcnow() - timedelta(hours=3),
                        mitigated_at=datetime.utcnow() - timedelta(hours=1) if is_mitigated else None
                    )
                    db.add(v)
                count += 1
        
        # Initial audit log
        audit = AuditLog(
            action="INITIALIZE_SOC_PLATFORM",
            actor="system_bootstrap",
            resource_type="SYSTEM",
            details={"platform": "AI SECURITY FASTER", "status": "ONLINE"}
        )
        db.add(audit)
        db.commit()
