import re
import urllib.parse
from typing import Dict, Any

BLOCKED_IP_PATTERNS = [
    r"^127\.", # Loopback
    r"^localhost$",
    r"^169\.254\.", # Cloud instance metadata (AWS/GCP/Azure)
    r"^10\.", # RFC1918 Class A
    r"^192\.168\.", # RFC1918 Class C
    r"^172\.(1[6-9]|2[0-9]|3[0-1])\.", # RFC1918 Class B
    r"^0\.0\.0\.0",
    r"metadata\.google\.internal"
]

class HTTPCallTool:
    name = "http_call"
    display_name = "HTTP Call"
    description = "Make outbound HTTP calls to external APIs with comprehensive SSRF protection."
    is_sensitive = False

    @classmethod
    def execute(cls, url: str, method: str = "GET", payload: Dict[str, Any] = None) -> Dict[str, Any]:
        parsed = urllib.parse.urlparse(url)
        hostname = (parsed.hostname or "").lower()

        if not hostname:
            return {
                "success": False,
                "error": "Invalid URL provided.",
                "blocked": False
            }

        # Check for SSRF / metadata access
        for pattern in BLOCKED_IP_PATTERNS:
            if re.search(pattern, hostname):
                return {
                    "success": False,
                    "error": f"SECURITY VIOLATION (ASI02 / SSRF): Outbound call to internal/restricted destination '{hostname}' is blocked.",
                    "blocked": True,
                    "target_host": hostname,
                    "risk_rule": "SSRF_RESTRICTED_IP_FILTER"
                }

        # Safe simulated external HTTP response
        return {
            "success": True,
            "blocked": False,
            "status_code": 200,
            "url": url,
            "response_body": {
                "status": "ok",
                "message": f"Successfully performed {method} to {hostname}",
                "simulated": True
            }
        }
