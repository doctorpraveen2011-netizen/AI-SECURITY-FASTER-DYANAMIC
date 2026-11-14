import re
import time
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from app.models.models import AgentExecution
from app.agent.tools.file_read import FileReadTool
from app.agent.tools.email_tool import EmailTool
from app.agent.tools.http_call import HTTPCallTool
from app.agent.tools.mcp_tool import MCPToolsConnector

class AgentRunner:
    @staticmethod
    def execute_task(
        db: Session,
        task: str,
        provider: str = "claude",
        model_name: str = "claude-3-5-sonnet-20241022",
        enabled_tools: List[str] = None,
        auto_approve_sensitive: bool = False
    ) -> Dict[str, Any]:
        enabled_tools = enabled_tools or ["file_read", "email", "http_call", "mcp_tools"]
        execution = AgentExecution(
            task_input=task,
            provider=provider,
            model_name=model_name,
            status="running",
            steps=[],
            security_alerts=[]
        )
        db.add(execution)
        db.commit()
        db.refresh(execution)

        steps = []
        alerts = []
        task_lower = task.lower()

        # Step 1: Initial Analysis & Plan
        steps.append({
            "step_number": 1,
            "thought": f"Analyzing task requirement: '{task}'. Determining required capabilities and security boundaries.",
            "tool": None,
            "tool_input": None,
            "tool_output": "Plan created: Verify safety constraints, select authorized tools, and execute sequential actions.",
            "is_sensitive": False
        })

        # Scenario 1: File reading requested (or path traversal attack probe)
        if "file" in task_lower or "read" in task_lower or "etc" in task_lower or "shadow" in task_lower or "passwd" in task_lower:
            # Extract target file or simulate attack payload
            if "shadow" in task_lower or "passwd" in task_lower or "win.ini" in task_lower or ".." in task:
                target_file = "../../../etc/shadow"
            else:
                target_file = "SEC-POL-001_Enterprise_AI_Security_Standard.md"

            res = FileReadTool.execute(target_file)
            step_record = {
                "step_number": len(steps) + 1,
                "thought": f"Invoking FileReadTool on target: {target_file}",
                "tool": "file_read",
                "tool_input": {"file_path": target_file},
                "tool_output": res,
                "is_sensitive": False
            }
            if res.get("blocked"):
                alerts.append({
                    "severity": "CRITICAL",
                    "code": "ASI02_PATH_TRAVERSAL",
                    "message": "Blocked unauthorized file traversal attempt outside sandbox perimeter."
                })
            steps.append(step_record)

        # Scenario 2: Network / HTTP Call (or SSRF probe)
        if "http" in task_lower or "fetch" in task_lower or "metadata" in task_lower or "169.254" in task_lower or "curl" in task_lower:
            if "metadata" in task_lower or "169.254" in task_lower or "localhost" in task_lower or "127.0.0.1" in task_lower:
                target_url = "http://169.254.169.254/latest/meta-data/"
            else:
                target_url = "https://api.github.com/zen"

            res = HTTPCallTool.execute(target_url)
            step_record = {
                "step_number": len(steps) + 1,
                "thought": f"Invoking HTTPCallTool with endpoint: {target_url}",
                "tool": "http_call",
                "tool_input": {"url": target_url},
                "tool_output": res,
                "is_sensitive": False
            }
            if res.get("blocked"):
                alerts.append({
                    "severity": "HIGH",
                    "code": "ASI02_SSRF_ATTEMPT",
                    "message": f"Blocked SSRF attempt targeting restricted host: {res.get('target_host')}."
                })
            steps.append(step_record)

        # Scenario 3: Email Dispatch (Requires Human Approval)
        if "email" in task_lower or "send" in task_lower or "notify" in task_lower or "dispatch" in task_lower:
            recipient = "secops-alert@enterprise.example.com"
            subject = "Automated AI Security Incident Report"
            body = f"Incident details for task: {task}"
            
            res = EmailTool.execute(recipient, subject, body, approved=auto_approve_sensitive)
            is_waiting = res.get("requires_approval", False)

            step_record = {
                "step_number": len(steps) + 1,
                "thought": "Drafting outgoing email alert. Human approval policy is enforced for external dispatch.",
                "tool": "email",
                "tool_input": {"recipient": recipient, "subject": subject, "body": body},
                "tool_output": res,
                "is_sensitive": True,
                "approval_status": "APPROVED" if auto_approve_sensitive else "WAITING_APPROVAL"
            }
            steps.append(step_record)

            if is_waiting:
                execution.status = "waiting_approval"
                execution.pending_tool_call = {
                    "tool": "email",
                    "arguments": {"recipient": recipient, "subject": subject, "body": body}
                }
                execution.steps = steps
                execution.security_alerts = alerts
                execution.result = "Execution suspended awaiting human approval for email dispatch."
                db.commit()
                return {
                    "execution_id": execution.id,
                    "status": "waiting_approval",
                    "steps": steps,
                    "security_alerts": alerts,
                    "pending_tool_call": execution.pending_tool_call,
                    "result": execution.result
                }

        # Scenario 4: MCP Tools
        if "mcp" in task_lower or "cluster" in task_lower or "system" in task_lower:
            res = MCPToolsConnector.execute("mcp_system_info", {})
            steps.append({
                "step_number": len(steps) + 1,
                "thought": "Querying connected MCP Gateway for system diagnostics.",
                "tool": "mcp_tools",
                "tool_input": {"tool_name": "mcp_system_info"},
                "tool_output": res,
                "is_sensitive": False
            })

        # Final Summary
        final_thought = "Task execution completed. Security invariants checked and logged to SOC audit stream."
        steps.append({
            "step_number": len(steps) + 1,
            "thought": final_thought,
            "tool": None,
            "tool_input": None,
            "tool_output": "Agent workflow successfully concluded within enforced security boundaries.",
            "is_sensitive": False
        })

        execution.status = "completed"
        execution.steps = steps
        execution.security_alerts = alerts
        execution.result = f"Completed agent workflow with {len(steps)} steps and {len(alerts)} security alerts."
        db.commit()

        return {
            "execution_id": execution.id,
            "status": execution.status,
            "steps": steps,
            "security_alerts": alerts,
            "pending_tool_call": None,
            "result": execution.result
        }

    @staticmethod
    def handle_approval(db: Session, execution_id: str, action: str, reason: str = None) -> Dict[str, Any]:
        execution = db.query(AgentExecution).filter(AgentExecution.id == execution_id).first()
        if not execution:
            return {"error": "Execution record not found"}

        if execution.status != "waiting_approval":
            return {"error": f"Execution is in '{execution.status}' state, not waiting approval."}

        steps = list(execution.steps or [])
        pending = execution.pending_tool_call or {}

        if action == "approve":
            # Dispatch approved tool
            if pending.get("tool") == "email":
                args = pending.get("arguments", {})
                res = EmailTool.execute(
                    args.get("recipient", "secops@example.com"),
                    args.get("subject", "Approved notification"),
                    args.get("body", ""),
                    approved=True
                )
                steps.append({
                    "step_number": len(steps) + 1,
                    "thought": "Human authorization received. Executing email dispatch to sandbox outbox.",
                    "tool": "email",
                    "tool_input": args,
                    "tool_output": res,
                    "is_sensitive": True,
                    "approval_status": "APPROVED"
                })
            execution.status = "completed"
            execution.result = "Human approved. Sensitive action executed successfully."
        else:
            steps.append({
                "step_number": len(steps) + 1,
                "thought": f"Human authorization REJECTED: {reason or 'Security engineer aborted operation.'}",
                "tool": pending.get("tool"),
                "tool_input": pending.get("arguments"),
                "tool_output": {"error": "Action aborted by human operator."},
                "is_sensitive": True,
                "approval_status": "REJECTED"
            })
            execution.status = "blocked"
            execution.result = f"Action rejected by human operator. Reason: {reason or 'Denied'}"

        execution.steps = steps
        execution.pending_tool_call = None
        db.commit()
        db.refresh(execution)

        return {
            "execution_id": execution.id,
            "status": execution.status,
            "steps": execution.steps,
            "result": execution.result
        }
