# Product Requirements Document (PRD)
## AI SECURITY FASTER – AI Red Teaming & Blue Teaming Operations Center

### 1. Executive Overview
**AI SECURITY FASTER** is an enterprise-grade AI Red Teaming and Blue Teaming Operations Center designed for continuous security testing, vulnerability evaluation, and defensive mitigation across Large Language Models (Anthropic Claude, Google Gemini) and autonomous Agentic AI systems.

Inspired by top-tier modern Security Operations Centers (SOC) and developer-first interfaces, AI Security Faster bridges the gap between offensive AI probing (Red Team) and automated defensive guardrails (Blue Team), providing quantifiable before-and-after verification metrics.

---

### 2. Target Personas
1. **AI Red Teamers & Penetration Testers**: Conduct automated and manual adversarial prompt injections, goal hijacking, and agentic exploitation campaigns against frontier models.
2. **AI Blue Team Engineers & Defensers**: Author, test, and deploy input/output guardrails, tool sandboxes, PII/secret redaction, and SSRF filters.
3. **CISO & AI Governance Officers**: Monitor OWASP LLM Top 10 and OWASP Agentic Security Initiative (ASI) compliance, generate executive compliance PDF/CSV/JSON audits, and monitor Wazuh SIEM alerts.

---

### 3. Core Functional Requirements

#### 3.1 Dual-Model Frontier AI Integration
- **Anthropic Claude**: Official Anthropic Python SDK (`anthropic`), supporting Claude 3.5 Sonnet, Claude 3 Haiku, and Claude 3 Opus via the Messages API with streaming, latency profiling, and token accounting.
- **Google Gemini**: Official Google Gen AI SDK (`google-genai` / `google-generativeai`), supporting Gemini 1.5 Pro, Gemini 1.5 Flash, and Gemini 2.0 with streaming and latency tracking.
- **Provider Switching**: Seamless 1-click toggle between Claude and Gemini in both chat and red team campaigns.
- **Side-by-side Comparative Evaluation**: Concurrent prompt execution to benchmark defense resilience and divergence.
- **Key & Health Management**: Live connection health-checking; transparent indication of unconfigured keys.

#### 3.2 Automated Red Team Engine (OFFENSIVE)
- **Taxonomy Compliance**:
  - **OWASP Top 10 for LLM Applications (2025/2026)**:
    - `LLM01`: Direct & Indirect Prompt Injection
    - `LLM02`: Sensitive Information Disclosure
    - `LLM03`: Supply Chain Vulnerabilities
    - `LLM08`: Excessive Agency
    - `LLM10`: Vector & Memory Misuse
  - **OWASP Agentic Security Initiative (ASI Top 10)**:
    - `ASI01`: Agent Goal Hijacking & Jailbreaking
    - `ASI02`: Tool Misuse & Parameter Tampering
    - `ASI03`: Identity & Privilege Abuse / Goal Misalignment
    - `ASI05`: Data Leakage & Context Poisoning
    - `ASI06`: Unexpected / Code Execution & Privilege Escalation
- **Coverage**: Minimum 3 distinct test cases per risk (30 test cases) executed across both Claude and Gemini = 60 test runs per full campaign.
- **Evidence Storage**: Persistent capture of prompt payloads, raw model outputs, observed vs expected behavior, CVSS severity, pass/fail status, and timestamped forensic logs.

#### 3.3 Blue Team Mitigation Engine (DEFENSIVE)
- **Real-Time Guardrails**:
  - Heuristic & Intent-based Prompt Injection Filter.
  - Secret & API Key Scanner (High-entropy tokens, AWS keys, JWTs, Anthropic/Google tokens).
  - PII Detection & Redaction (SSNs, credit cards, emails, phone numbers).
  - Agent Tool Execution Allowlist & Sandboxing.
  - SSRF Protection (Block internal IPs: `127.0.0.1`, `169.254.169.254`, `10.0.0.0/8`, `192.168.0.0/16`).
  - Path Traversal Sanitizer (Blocks `../`, `..\\`, absolute root paths).
  - Human-in-the-Loop (HITL) approval gate for sensitive actions (e.g. Email dispatch, external HTTP, file mutation).
- **Mandatory Before-and-After Workflow**:
  - Attack Execution (Vulnerability Confirmed) -> Apply Guardrail -> Retest Identical Payload -> Verify Mitigation -> Update Risk Score. Only verified retests transition vulnerabilities to "Mitigated".

#### 3.4 AI Agent Lab
- Autonomous agent test harness equipped with 4 sandboxed tools:
  1. `File Read`: Sandboxed directory reading with strict path traversal protections.
  2. `Email`: Sandboxed email drafting with mandatory human authorization dialog before mock dispatch.
  3. `HTTP Call`: Controlled outbound caller with URL allowlisting and cloud metadata/SSRF filters.
  4. `MCP Tools`: Model Context Protocol integration supporting dynamic tool schema discovery and execution.
- Step-by-step audit logging of reasoning traces, tool parameters, approvals, and security alerts.

#### 3.5 Model Context Protocol (MCP) Security Lab
- Embedded local MCP test server with tools for synthetic file browsing and system diagnostics.
- Proof of Concept (PoC) security test cases:
  - Unauthorized tool execution attempt.
  - Path traversal payload (`../../../etc/shadow` / `..\..\..\windows\win.ini`).
  - Excessive permission escalation.
  - Argument poisoning.
- Live visualization of connection risk score (e.g., 11% Connection Secure) and audit trail.

#### 3.6 Enterprise Knowledge Base & RAG
- Shared document ingestion (PDF, DOCX, TXT, Markdown).
- Text chunking with semantic embeddings.
- Vector similarity search (pgvector / cosine vector store) with citation metadata.
- Pre-seeded with synthetic corporate security test data (confidential customer records, internal passwords, API canary tokens).

#### 3.7 Wazuh SIEM Integration
- Wazuh Manager API configuration, TLS authentication, and health checking.
- Ingestion and correlation of active security alerts (e.g. agent tool exploitation, suspicious HTTP probes).
- Live feed of alert severity, agent status, and rule IDs.

#### 3.8 Analytics, Live Dashboard & Reporting
- Pixel-perfect recreation of SOC Dashboard:
  - Total Tests Run, Vulnerabilities Found, Mitigated Risks, Avg Scan Time.
  - Models & Tools status card.
  - Risk Coverage (OWASP 2026 matrix).
  - Attack Test Cases status bars.
  - Before/After Mitigation Results table.
  - MCP Connection Risk widget with PoC status badge.
  - Interactive Recharts Test Reports trend.
- Export options: Comprehensive PDF Security Report, CSV export, and JSON dump.
- Complete Audit Log view.

---

### 4. Non-Functional Requirements
- **Performance**: Sub-100ms API response latency for cached metrics; real-time streaming for LLM tokens.
- **Security**: Zero client-side API key leakage. Environment-driven secret management.
- **Reliability**: Dual-engine persistence (PostgreSQL with SQLite fallback for zero-dependency local runs).
- **Design System**: Dark theme (`#0A0A0C` background, `#14161D` card surface, `#FF8A00` vibrant orange accent, LeetCode/SOC aesthetic).
