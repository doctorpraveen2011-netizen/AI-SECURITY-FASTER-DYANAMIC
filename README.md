# AI SECURITY FASTER – Operations Center
### Enterprise AI Red Teaming & Blue Teaming Operations Center
Repository: [AI-SECURITY-FASTER-DYANAMIC](https://github.com/doctorpraveen2011-netizen/AI-SECURITY-FASTER-DYANAMIC)

[![OWASP 2026 Compliant](https://img.shields.io/badge/OWASP-LLM%20%26%20ASI%202026-FF8A00)](https://owasp.org/)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20TypeScript-61DAFB)](https://react.dev/)
[![Anthropic Claude](https://img.shields.io/badge/Frontier%20LLM-Claude%203.5-orange)](https://docs.anthropic.com/)
[![Google Gemini](https://img.shields.io/badge/Frontier%20LLM-Gemini%201.5%2F2.0-blue)](https://ai.google.dev/)

---

## 1. Project Overview

**AI SECURITY FASTER** is an enterprise-grade AI Red Teaming and Blue Teaming Operations Center designed for continuous security testing, vulnerability evaluation, and defensive mitigation across Large Language Models (Anthropic Claude, Google Gemini) and autonomous Agentic AI workflows.

The application features:
- **Deep Obsidian Black & Neon Orange Glowing Aesthetic (`#FF8A00`)**: Designed with LeetCode-grade responsiveness and modern cybersecurity SOC appearance.
- **Dual-Model Frontier Integration**: Official Anthropic Claude Messages API and Google Gen AI Gemini API integration with streaming, token accounting, latency metrics, and side-by-side comparative testing.
- **Shared Enterprise RAG Knowledge Base**: Vector retrieval pre-seeded with synthetic corporate security test data.
- **Sandboxed AI Agent Lab**: 4 specialized agent tools (File Read with path traversal protection, Email with mandatory Human-in-the-Loop approval, HTTP Call with SSRF filter, and MCP Tools).
- **Automated Red Team Engine**: 10 official OWASP risk categories (5 LLM, 5 Agentic) with 3 distinct test cases each, executing 60 model-specific tests per full campaign.
- **Blue Team Mitigation Engine**: Mandatory before-and-after retest verification workflow.
- **MCP Security Lab**: Local MCP server and client with PoC path traversal and unauthorized tool call defense.
- **Wazuh SIEM Integration**: Live telemetry and correlation interface.
- **Full Reporting**: Automated publication-grade PDF, CSV, and JSON security audits.

---

## 2. Architecture & File Structure

```text
ai-security-faster/
├── backend/
│   ├── app/
│   │   ├── api/                 # REST routes (dashboard, llm, agent, redteam, blueteam, mcp, wazuh, reports)
│   │   ├── core/                # Configuration and environment settings
│   │   ├── database/            # SQLAlchemy session, engine, dynamic sqlite/postgres
│   │   ├── models/              # SQLAlchemy declarative models
│   │   ├── schemas/             # Pydantic validation schemas
│   │   ├── llm/                 # Claude & Gemini providers, router, streaming
│   │   ├── rag/                 # Document parsing, chunking, embeddings, similarity search
│   │   ├── agent/               # Sandboxed Agent, 4 tools, human approval gate
│   │   ├── redteam/             # OWASP 2026 test suites (LLM01-10, ASI01-06)
│   │   ├── blueteam/            # Guardrails, input/output scanners, retesting
│   │   ├── mcp/                 # Local MCP server, client, security PoC harness
│   │   ├── wazuh/               # Wazuh API client & alert aggregator
│   │   └── reporting/           # ReportLab PDF, CSV, JSON export engines
│   ├── requirements.txt
│   ├── run_backend.py
│   └── seed_data.py
├── frontend/
│   ├── src/
│   │   ├── components/          # Reusable SOC components, charts, modals, brain graphic
│   │   ├── pages/               # 12 functional page views
│   │   ├── services/            # Axios / Fetch API clients for backend
│   │   ├── types/               # TypeScript interfaces matching backend schemas
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   ├── tailwind.config.js
│   └── vite.config.ts
├── docker-compose.yml
├── .env.example
├── run_backend.py
├── prd.md
├── rules.md
├── tasks.md
├── design.md
├── system_architecture.md
├── memory.md
└── research.md
```

---

## 3. Quick Start (Local VS Code Execution)

### Step 1: Start the Backend Server

```bash
# Activate virtual environment
.\backend\venv\Scripts\activate

# Run backend server (FastAPI on http://127.0.0.1:8000)
python run_backend.py
```

The database (`ai_security.db`) is automatically initialized and seeded with OWASP risk categories, test cases, and initial metrics.

### Step 2: Start the Frontend Dev Server

```bash
# In another terminal:
npm run dev --prefix frontend
```

Open **http://localhost:5173** in your browser to access the AI Security Faster Operations Center!

### Step 3 (Optional): Docker Compose Deployment

```bash
docker-compose up --build
```

---

## 4. OWASP 2026 Risk Matrix

| Risk ID | Framework | Vulnerability Category | Severity | Tests |
| :--- | :--- | :--- | :--- | :--- |
| **LLM01** | OWASP LLM 2026 | Direct & Indirect Prompt Injection | CRITICAL | 3 Tests |
| **LLM02** | OWASP LLM 2026 | Sensitive Information Disclosure | HIGH | 3 Tests |
| **LLM03** | OWASP LLM 2026 | Supply Chain Vulnerabilities | HIGH | 3 Tests |
| **LLM08** | OWASP LLM 2026 | Excessive Agency | CRITICAL | 3 Tests |
| **LLM10** | OWASP LLM 2026 | Vector and Memory Misuse | HIGH | 3 Tests |
| **ASI01** | OWASP ASI 2026 | Agent Goal Hijack & Jailbreak | CRITICAL | 3 Tests |
| **ASI02** | OWASP ASI 2026 | Tool Misuse & Parameter Tampering | HIGH | 3 Tests |
| **ASI03** | OWASP ASI 2026 | Identity & Privilege Abuse | HIGH | 3 Tests |
| **ASI05** | OWASP ASI 2026 | Data Leakage & Context Poisoning | MEDIUM | 3 Tests |
| **ASI06** | OWASP ASI 2026 | Unexpected Code Execution | CRITICAL | 3 Tests |

Total test cases: **30 distinct tests × 2 models = 60 test executions per full campaign**.

---

## 5. Security & Verification Engine

1. **Before-and-After Retest Policy**:
   Mitigations are never assumed. The platform executes the exact adversarial payload against the defended pipeline, confirms sanitation or blocking, and transitions status to `VERIFIED`.
2. **SSRF Barrier**:
   Outbound HTTP caller actively blocks cloud metadata (`169.254.169.254`), loopback (`127.0.0.1`), and RFC1918 private subnets.
3. **Path Traversal Barrier**:
   File read operations are strictly resolved against `/sandbox_data/` and prohibit relative directory traversal sequences (`../`).
4. **Human-in-the-Loop Gate**:
   Privileged actions (external email dispatch, code evaluation) halt execution state and require security engineer authorization.
>>>>>>> b76cc77 (feat: complete AI SECURITY FASTER enterprise platform implementation)
