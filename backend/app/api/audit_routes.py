from typing import List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.models import AuditLog

router = APIRouter(prefix="/audit", tags=["Audit Logs"])

@router.get("/logs")
def list_audit_logs(limit: int = 50, db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(limit).all()
    return [{
        "id": l.id,
        "action": l.action,
        "actor": l.actor,
        "resource_type": l.resource_type,
        "resource_id": l.resource_id,
        "details": l.details,
        "ip_address": l.ip_address,
        "timestamp": l.timestamp.isoformat()
    } for l in logs]
