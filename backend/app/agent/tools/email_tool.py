from typing import Dict, Any

class EmailTool:
    name = "email"
    display_name = "Email Dispatch"
    description = "Draft and queue outgoing emails. Sensitive tool: requires human approval before sending."
    is_sensitive = True

    @classmethod
    def execute(cls, recipient: str, subject: str, body: str, approved: bool = False) -> Dict[str, Any]:
        if not approved:
            return {
                "success": False,
                "requires_approval": True,
                "pending_action": "DISPATCH_EMAIL",
                "recipient": recipient,
                "subject": subject,
                "body_preview": body[:150] + ("..." if len(body) > 150 else ""),
                "message": "Human approval required before dispatching email to external recipient."
            }

        # Simulated sandbox email delivery
        return {
            "success": True,
            "requires_approval": False,
            "dispatched": True,
            "recipient": recipient,
            "subject": subject,
            "status": "DELIVERED_TO_SANDBOX_OUTBOX",
            "message": f"Email successfully sent to sandbox outbox for {recipient}."
        }
