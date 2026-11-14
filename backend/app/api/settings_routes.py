import os
from pydantic import BaseModel
from typing import Optional
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.llm.llm_router import llm_router
from app.models.models import AuditLog
from app.database.session import get_db

router = APIRouter(prefix="/settings", tags=["Settings"])

class SettingsUpdateRequest(BaseModel):
    anthropic_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    wazuh_api_url: Optional[str] = None
    wazuh_api_user: Optional[str] = None
    wazuh_api_password: Optional[str] = None

def mask_key(k: Optional[str]) -> str:
    if not k or len(k) < 8:
        return ""
    return f"{k[:4]}...{k[-4:]}"

@router.get("/")
def get_current_settings():
    return {
        "anthropic_configured": bool(settings.ANTHROPIC_API_KEY),
        "anthropic_masked": mask_key(settings.ANTHROPIC_API_KEY),
        "gemini_configured": bool(settings.GEMINI_API_KEY),
        "gemini_masked": mask_key(settings.GEMINI_API_KEY),
        "wazuh_api_url": settings.WAZUH_API_URL,
        "database_url": settings.DATABASE_URL.split("@")[-1] if "@" in settings.DATABASE_URL else settings.DATABASE_URL,
        "default_claude_model": settings.DEFAULT_CLAUDE_MODEL,
        "default_gemini_model": settings.DEFAULT_GEMINI_MODEL
    }

@router.post("/update")
def update_settings(req: SettingsUpdateRequest, db: Session = Depends(get_db)):
    if req.anthropic_api_key is not None and req.anthropic_api_key.strip():
        settings.ANTHROPIC_API_KEY = req.anthropic_api_key.strip()
        llm_router.update_keys(anthropic_key=settings.ANTHROPIC_API_KEY)
    
    if req.gemini_api_key is not None and req.gemini_api_key.strip():
        settings.GEMINI_API_KEY = req.gemini_api_key.strip()
        llm_router.update_keys(gemini_key=settings.GEMINI_API_KEY)

    if req.wazuh_api_url is not None and req.wazuh_api_url.strip():
        settings.WAZUH_API_URL = req.wazuh_api_url.strip()

    log = AuditLog(
        action="UPDATE_SECURITY_SETTINGS",
        actor="security_engineer",
        resource_type="CONFIGURATION",
        details={"keys_updated": True}
    )
    db.add(log)
    db.commit()

    return {
        "status": "success",
        "message": "Settings updated successfully.",
        "settings": get_current_settings()
    }
