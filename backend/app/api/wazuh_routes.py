from fastapi import APIRouter
from app.wazuh.wazuh_client import wazuh_client

router = APIRouter(prefix="/wazuh", tags=["Wazuh Integration"])

@router.get("/status")
async def get_wazuh_status():
    return await wazuh_client.check_connection()

@router.get("/alerts")
async def get_wazuh_alerts(limit: int = 20):
    return await wazuh_client.get_alerts(limit=limit)
