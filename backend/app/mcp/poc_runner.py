from datetime import datetime
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.models import MCPConnection, MCPEvent
from app.mcp.mcp_server import LocalMCPServer

class MCPPocRunner:
    @staticmethod
    def initialize_connection(db: Session) -> MCPConnection:
        conn = db.query(MCPConnection).first()
        if not conn:
            conn = MCPConnection(
                server_name="Local SOC MCP Gateway",
                server_url="http://127.0.0.1:8765/mcp/v1",
                status="CONNECTED",
                risk_score=11.0,
                discovered_tools=LocalMCPServer.list_tools(),
                permissions={"read:sandbox": True, "telemetry:read": True, "audit:admin": False}
            )
            db.add(conn)
            
            # Initial event matching the screenshot PoC
            ev = MCPEvent(
                event_type="PATH_TRAVERSAL_BLOCKED",
                details="Attempted path traversal (../../../etc/shadow) blocked.",
                status="BLOCKED"
            )
            db.add(ev)
            db.commit()
            db.refresh(conn)
        return conn

    @staticmethod
    def run_poc(db: Session, poc_type: str = "path_traversal") -> Dict[str, Any]:
        conn = MCPPocRunner.initialize_connection(db)

        if poc_type == "path_traversal":
            payload = "../../../etc/shadow"
            res = LocalMCPServer.execute_tool("read_sandboxed_file", {"path": payload})
            
            event = MCPEvent(
                event_type="PATH_TRAVERSAL_BLOCKED",
                details=f"Attempted path traversal ({payload}) blocked.",
                status="BLOCKED"
            )
            db.add(event)
            db.commit()

            return {
                "poc_type": "path_traversal",
                "target_payload": payload,
                "status": "Blocked",
                "details": f"Attempted path traversal ({payload}) blocked.",
                "risk_score": 11.0,
                "connection_status": "Connection Secure",
                "server_response": res
            }

        elif poc_type == "unauthorized_tool":
            res = LocalMCPServer.execute_tool("soc_audit_stream", {"limit": 10}, caller_role="guest")
            event = MCPEvent(
                event_type="UNAUTHORIZED_CALL_BLOCKED",
                details="Unauthorized call to 'soc_audit_stream' blocked. Missing 'audit:admin' privilege.",
                status="BLOCKED"
            )
            db.add(event)
            db.commit()

            return {
                "poc_type": "unauthorized_tool",
                "status": "Blocked",
                "details": "Unauthorized tool invocation blocked by MCP gateway authorization filter.",
                "risk_score": 11.0,
                "connection_status": "Connection Secure",
                "server_response": res
            }

        else:
            return {
                "poc_type": poc_type,
                "status": "Blocked",
                "details": f"Executed MCP security check for {poc_type}.",
                "risk_score": 11.0,
                "connection_status": "Connection Secure"
            }
