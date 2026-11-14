import httpx
from typing import Dict, Any, List
from app.core.config import settings

class WazuhClient:
    def __init__(self):
        self.api_url = settings.WAZUH_API_URL.rstrip("/")
        self.user = settings.WAZUH_API_USER
        self.password = settings.WAZUH_API_PASSWORD
        self.verify_ssl = settings.WAZUH_VERIFY_SSL

    async def check_connection(self) -> Dict[str, Any]:
        if not self.api_url or self.api_url.startswith("https://127.0.0.1:55000"):
            # Check if default local server actually responds or if unconfigured
            try:
                async with httpx.AsyncClient(verify=self.verify_ssl, timeout=2.0) as client:
                    res = await client.get(f"{self.api_url}/")
                    return {
                        "status": "connected",
                        "api_url": self.api_url,
                        "message": "Connected to Wazuh Manager API",
                        "status_code": res.status_code
                    }
            except Exception:
                return {
                    "status": "unconfigured",
                    "api_url": self.api_url,
                    "message": "Wazuh SIEM Manager not detected at configured endpoint. Set WAZUH_API_URL in Settings.",
                    "authenticated": False
                }

        try:
            async with httpx.AsyncClient(verify=self.verify_ssl, timeout=3.0) as client:
                res = await client.get(
                    f"{self.api_url}/security/user/authenticate",
                    auth=(self.user, self.password)
                )
                if res.status_code == 200:
                    return {
                        "status": "connected",
                        "api_url": self.api_url,
                        "message": "Wazuh API Authenticated & Active",
                        "authenticated": True
                    }
                else:
                    return {
                        "status": "error",
                        "api_url": self.api_url,
                        "message": f"Wazuh Auth failed with HTTP {res.status_code}",
                        "authenticated": False
                    }
        except Exception as e:
            return {
                "status": "disconnected",
                "api_url": self.api_url,
                "message": f"Could not reach Wazuh Manager: {str(e)}",
                "authenticated": False
            }

    async def get_alerts(self, limit: int = 20) -> List[Dict[str, Any]]:
        conn = await self.check_connection()
        if conn["status"] != "connected":
            # Rule: Never display fabricated Wazuh alerts!
            return []

        # If connected to live Wazuh, query alerts
        try:
            async with httpx.AsyncClient(verify=self.verify_ssl, timeout=4.0) as client:
                # In real Wazuh, GET /security/user/authenticate returns token, then GET /alerts
                auth_res = await client.post(
                    f"{self.api_url}/security/user/authenticate",
                    auth=(self.user, self.password)
                )
                token = auth_res.json().get("data", {}).get("token")
                headers = {"Authorization": f"Bearer {token}"} if token else {}
                
                alerts_res = await client.get(
                    f"{self.api_url}/alerts?limit={limit}",
                    headers=headers
                )
                if alerts_res.status_code == 200:
                    data = alerts_res.json().get("data", {}).get("affected_items", [])
                    return data
                return []
        except Exception:
            return []

wazuh_client = WazuhClient()
