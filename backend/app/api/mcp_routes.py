from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.schemas import MCPToolExecuteRequest, MCPPoCRunRequest
from app.mcp.mcp_server import LocalMCPServer
from app.mcp.poc_runner import MCPPocRunner
from app.models.models import MCPConnection, MCPEvent

router = APIRouter(prefix="/mcp", tags=["MCP Security Lab"])

@router.get("/status")
def get_mcp_status(db: Session = Depends(get_db)):
    conn = MCPPocRunner.initialize_connection(db)
    server_meta = LocalMCPServer.get_server_metadata()
    latest_events = db.query(MCPEvent).order_by(MCPEvent.created_at.desc()).limit(10).all()
    
    return {
        "server": server_meta,
        "connection_secure": True,
        "risk_score": conn.risk_score,
        "discovered_tools": LocalMCPServer.list_tools(),
        "recent_security_events": [{
            "id": ev.id,
            "type": ev.event_type,
            "details": ev.details,
            "status": ev.status,
            "timestamp": ev.created_at.isoformat()
        } for ev in latest_events]
    }

@router.post("/poc")
def run_mcp_poc(request: MCPPoCRunRequest, db: Session = Depends(get_db)):
    return MCPPocRunner.run_poc(db, poc_type=request.poc_type)

@router.post("/execute")
def execute_mcp_tool(request: MCPToolExecuteRequest):
    return LocalMCPServer.execute_tool(request.tool_name, request.arguments)
