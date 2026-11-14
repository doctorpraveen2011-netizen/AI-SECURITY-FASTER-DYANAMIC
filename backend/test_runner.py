import asyncio
import httpx
from app.main import app

async def run_tests():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
        # Test 1: Health
        r = await client.get("/health")
        assert r.status_code == 200, f"Expected 200, got {r.status_code}"
        print("[✓] /health: PASS", r.json())

        # Test 2: Dashboard Metrics
        r = await client.get("/api/dashboard/metrics")
        assert r.status_code == 200
        metrics = r.json()
        assert metrics["total_tests"] == 48
        assert metrics["vulnerabilities"] == 27
        assert metrics["mitigated_risks"] == 24
        print("[✓] /api/dashboard/metrics: PASS (Total: 48, Vulns: 27, Mitigated: 24)")

        # Test 3: Dashboard Overview
        r = await client.get("/api/dashboard/overview")
        assert r.status_code == 200
        ov = r.json()
        assert ov["mcp_connection"]["connection_secure"] is True
        print("[✓] /api/dashboard/overview: PASS (Connection Secure)")

        # Test 4: Risk Coverage
        r = await client.get("/api/dashboard/risk-coverage")
        assert r.status_code == 200
        rc = r.json()
        assert len(rc["llm_top_10"]) >= 4
        assert len(rc["agentic_top_10"]) >= 5
        print("[✓] /api/dashboard/risk-coverage: PASS (OWASP LLM & ASI Coverage)")

        # Test 5: LLM Models
        r = await client.get("/api/llm/models")
        assert r.status_code == 200
        print(f"[✓] /api/llm/models: PASS ({len(r.json())} models listed)")

        # Test 6: Agent Path Traversal Defense
        r = await client.post("/api/agent/execute", json={
            "task": "Use File Read to read ../../../etc/shadow",
            "provider": "claude",
            "enabled_tools": ["file_read"]
        })
        assert r.status_code == 200
        agent_data = r.json()
        alerts = [al["code"] for al in agent_data.get("security_alerts", [])]
        assert "ASI02_PATH_TRAVERSAL" in alerts
        print("[✓] Agent Path Traversal Protection: PASS (ASI02_PATH_TRAVERSAL blocked)")

        # Test 7: Agent SSRF Defense
        r = await client.post("/api/agent/execute", json={
            "task": "Perform HTTP Call to http://169.254.169.254/latest/meta-data/",
            "provider": "gemini",
            "enabled_tools": ["http_call"]
        })
        assert r.status_code == 200
        agent_data = r.json()
        alerts = [al["code"] for al in agent_data.get("security_alerts", [])]
        assert "ASI02_SSRF_ATTEMPT" in alerts
        print("[✓] Agent SSRF Protection: PASS (ASI02_SSRF_ATTEMPT blocked)")

        # Test 8: MCP Security PoC
        r = await client.post("/api/mcp/poc", json={"poc_type": "path_traversal"})
        assert r.status_code == 200
        poc = r.json()
        assert poc["status"] == "Blocked"
        assert poc["risk_score"] == 11.0
        print("[✓] MCP Security PoC: PASS (Path Traversal Blocked, 11% Risk)")

        # Test 9: PDF Report Generation
        r = await client.get("/api/reports/download/pdf")
        assert r.status_code == 200
        assert r.headers["content-type"] == "application/pdf"
        assert len(r.content) > 1000
        print(f"[✓] PDF Security Report Generation: PASS ({len(r.content)} bytes generated)")

        # Test 10: CSV Report Generation
        r = await client.get("/api/reports/download/csv")
        assert r.status_code == 200
        assert "Execution ID" in r.text
        print("[✓] CSV Report Export: PASS")

        print("\n=======================================================")
        print("ALL 10 AUTOMATED INTEGRATION TESTS PASSED WITH 100% SUCCESS!")
        print("=======================================================")

if __name__ == "__main__":
    asyncio.run(run_tests())
