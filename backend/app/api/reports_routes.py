import csv
import io
import json
from datetime import datetime
from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import Vulnerability, Mitigation, TestExecution
from app.reporting.pdf_generator import PDFReportGenerator
from app.api.dashboard import get_dashboard_metrics, get_dashboard_mitigations

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/download/pdf")
def download_pdf_report(db: Session = Depends(get_db)):
    metrics = get_dashboard_metrics(db)
    mitigations = get_dashboard_mitigations(db).get("items", [])
    vulns = db.query(Vulnerability).all()
    tests = db.query(TestExecution).limit(20).all()

    pdf_buffer = PDFReportGenerator.generate_security_report(
        metrics=metrics,
        mitigations=mitigations,
        vulnerabilities=vulns,
        test_summary=tests
    )

    filename = f"AI_Security_Faster_Audit_Report_{datetime.utcnow().strftime('%Y%m%d_%H%M')}.pdf"
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/download/csv")
def download_csv_report(db: Session = Depends(get_db)):
    tests = db.query(TestExecution).order_by(TestExecution.executed_at.desc()).all()
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "Execution ID", "Test Case ID", "Provider", "Model",
        "Result", "Severity", "Latency (ms)", "Executed At"
    ])
    for t in tests:
        writer.writerow([
            t.id, t.test_case_id, t.provider, t.model_name,
            t.result, t.severity, t.latency_ms, t.executed_at.isoformat()
        ])
    
    output.seek(0)
    filename = f"AI_Security_Faster_Tests_{datetime.utcnow().strftime('%Y%m%d')}.csv"
    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )

@router.get("/download/json")
def download_json_report(db: Session = Depends(get_db)):
    tests = db.query(TestExecution).all()
    vulns = db.query(Vulnerability).all()
    mits = db.query(Mitigation).all()

    data = {
        "platform": "AI SECURITY FASTER",
        "generated_at": datetime.utcnow().isoformat(),
        "summary": get_dashboard_metrics(db),
        "test_executions": [{
            "id": t.id,
            "test_case_id": t.test_case_id,
            "provider": t.provider,
            "result": t.result,
            "severity": t.severity,
            "latency_ms": t.latency_ms
        } for t in tests],
        "vulnerabilities": [{
            "id": v.id,
            "risk_id": v.risk_id,
            "title": v.title,
            "severity": v.severity,
            "status": v.status
        } for v in vulns],
        "mitigations": [{
            "id": m.id,
            "name": m.name,
            "status": m.verification_status,
            "reduction": f"{m.before_risk_pct}% -> {m.after_risk_pct}%"
        } for m in mits]
    }

    filename = f"AI_Security_Faster_Export_{datetime.utcnow().strftime('%Y%m%d')}.json"
    return Response(
        content=json.dumps(data, indent=2),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
