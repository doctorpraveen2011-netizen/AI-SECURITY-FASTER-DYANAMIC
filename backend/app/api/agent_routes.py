from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.schemas import AgentExecutionRequest, AgentApprovalRequest
from app.agent.agent_runner import AgentRunner
from app.agent.tools.mcp_tool import MCPToolsConnector
from app.models.models import AgentExecution

router = APIRouter(prefix="/agent", tags=["AI Agent Lab"])

@router.get("/tools")
def list_available_tools():
    return [
        {
            "id": "file_read",
            "name": "File Read",
            "description": "Sandboxed file access restricted to authorized folder with path traversal protection.",
            "is_sensitive": False,
            "requires_approval": False
        },
        {
            "id": "email",
            "name": "Email",
            "description": "Drafting and outbound sandbox email integration. Sensitive: requires human approval before sending.",
            "is_sensitive": True,
            "requires_approval": True
        },
        {
            "id": "http_call",
            "name": "HTTP Call",
            "description": "Controlled outbound HTTP requests with comprehensive SSRF and cloud metadata protection.",
            "is_sensitive": False,
            "requires_approval": False
        },
        {
            "id": "mcp_tools",
            "name": "MCP Tools",
            "description": "Model Context Protocol gateway for discoverable tools and system telemetry.",
            "is_sensitive": True,
            "requires_approval": False
        }
    ]

@router.post("/execute")
def execute_agent_task(
    request: AgentExecutionRequest,
    db: Session = Depends(get_db)
):
    result = AgentRunner.execute_task(
        db=db,
        task=request.task,
        provider=request.provider,
        model_name=request.model_name or "claude-3-5-sonnet-20241022",
        enabled_tools=request.enabled_tools,
        auto_approve_sensitive=request.auto_approve_sensitive
    )
    return result

@router.post("/approve")
def handle_agent_approval(
    request: AgentApprovalRequest,
    db: Session = Depends(get_db)
):
    res = AgentRunner.handle_approval(
        db=db,
        execution_id=request.execution_id,
        action=request.action,
        reason=request.rejection_reason
    )
    if "error" in res:
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@router.get("/executions")
def list_executions(limit: int = 15, db: Session = Depends(get_db)):
    execs = db.query(AgentExecution).order_by(AgentExecution.created_at.desc()).limit(limit).all()
    return [{
        "id": e.id,
        "task_input": e.task_input,
        "provider": e.provider,
        "model_name": e.model_name,
        "status": e.status,
        "steps_count": len(e.steps or []),
        "alerts_count": len(e.security_alerts or []),
        "pending_tool_call": e.pending_tool_call,
        "created_at": e.created_at.isoformat()
    } for e in execs]

@router.get("/executions/{execution_id}")
def get_execution_detail(execution_id: str, db: Session = Depends(get_db)):
    e = db.query(AgentExecution).filter(AgentExecution.id == execution_id).first()
    if not e:
        raise HTTPException(status_code=404, detail="Execution not found")
    return {
        "id": e.id,
        "task_input": e.task_input,
        "provider": e.provider,
        "model_name": e.model_name,
        "status": e.status,
        "steps": e.steps,
        "security_alerts": e.security_alerts,
        "pending_tool_call": e.pending_tool_call,
        "result": e.result,
        "created_at": e.created_at.isoformat()
    }
