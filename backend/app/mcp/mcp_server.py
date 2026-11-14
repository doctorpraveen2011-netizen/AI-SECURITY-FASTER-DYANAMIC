import os
from pathlib import Path
from typing import Dict, Any, List
from app.core.config import settings

class LocalMCPServer:
    """
    Local Model Context Protocol (MCP) server implementation.
    Exposes tools for discovery, schema inspection, and permissioned execution.
    """
    SERVER_NAME = "local-soc-mcp-gateway"
    PROTOCOL_VERSION = "2024-11-05"

    TOOLS_REGISTRY = [
        {
            "name": "read_sandboxed_file",
            "description": "Read file contents from the authorized SOC sandbox repository.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Relative path to file"}
                },
                "required": ["path"]
            },
            "required_permission": "file:read:sandbox"
        },
        {
            "name": "system_diagnostics",
            "description": "Collect local cluster telemetry and resource utilization.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "verbose": {"type": "boolean", "default": False}
                }
            },
            "required_permission": "telemetry:read"
        },
        {
            "name": "soc_audit_stream",
            "description": "Stream raw SIEM audit event logs.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "limit": {"type": "integer", "default": 10}
                }
            },
            "required_permission": "audit:admin"
        }
    ]

    @classmethod
    def get_server_metadata(cls) -> Dict[str, Any]:
        return {
            "name": cls.SERVER_NAME,
            "version": "1.0.0",
            "protocol_version": cls.PROTOCOL_VERSION,
            "transport": "in-process / stdio / sse",
            "status": "ONLINE",
            "authenticated": True,
            "tools_count": len(cls.TOOLS_REGISTRY)
        }

    @classmethod
    def list_tools(cls) -> List[Dict[str, Any]]:
        return cls.TOOLS_REGISTRY

    @classmethod
    def execute_tool(cls, tool_name: str, arguments: Dict[str, Any], caller_role: str = "security_engineer") -> Dict[str, Any]:
        matched = next((t for t in cls.TOOLS_REGISTRY if t["name"] == tool_name), None)
        if not matched:
            return {
                "success": False,
                "error": f"Tool '{tool_name}' is not registered on this MCP server.",
                "blocked": True
            }

        # Permission check
        if matched["required_permission"] == "audit:admin" and caller_role != "admin":
            return {
                "success": False,
                "error": "SECURITY VIOLATION (MCP-002): Unauthorized tool call. Caller lacks 'audit:admin' capability.",
                "blocked": True,
                "code": "INSUFFICIENT_PERMISSIONS"
            }

        if tool_name == "read_sandboxed_file":
            req_path = arguments.get("path", "")
            # Path traversal detection
            if ".." in req_path or req_path.startswith("/") or req_path.startswith("\\") or ":" in req_path:
                return {
                    "success": False,
                    "error": f"SECURITY VIOLATION (MCP-001): Attempted path traversal ({req_path}) blocked. Sandbox containment violation.",
                    "blocked": True,
                    "code": "PATH_TRAVERSAL_DETECTED",
                    "attempted_path": req_path
                }
            
            target = (settings.SANDBOX_DIR / req_path).resolve()
            if not str(target).startswith(str(settings.SANDBOX_DIR.resolve())):
                return {
                    "success": False,
                    "error": f"Path traversal escape blocked: {req_path}",
                    "blocked": True
                }

            if not target.exists():
                return {"success": False, "error": f"File '{req_path}' not found in sandbox."}

            with open(target, "r", encoding="utf-8", errors="ignore") as f:
                return {"success": True, "content": f.read()[:2000], "path": req_path}

        elif tool_name == "system_diagnostics":
            return {
                "success": True,
                "diagnostics": {
                    "uptime": "99.98%",
                    "cpu_percent": 14.2,
                    "memory_mb": 420.5,
                    "active_connections": 1,
                    "mcp_security_posture": "SECURE"
                }
            }

        return {"success": True, "result": f"Executed {tool_name}."}
