# Tasks & Implementation Roadmap
## AI SECURITY FASTER – AI Red Teaming & Blue Teaming Operations Center

### Phase 1: Architecture, Documentation & Environment Setup
- [x] Create core specifications: `prd.md`, `rules.md`, `tasks.md`, `design.md`, `system_architecture.md`, `memory.md`, `research.md`.
- [x] Inspect local runtime environment (Node 24, Python 3.14, npm).
- [ ] Initialize Python backend with virtual environment, FastAPI, SQLAlchemy, Pydantic, Anthropic SDK, Google Gen AI SDK.
- [ ] Initialize React + TypeScript + Vite frontend with Tailwind CSS, Lucide React, Recharts.

### Phase 2: Database Schema & Core Storage
- [ ] Define SQLAlchemy database models:
  - Users, ModelConfigs, Conversations, Messages
  - KnowledgeDocs, DocumentChunks
  - Agents, AgentTools, AgentExecutions
  - AttackCampaigns, RiskCategories, AttackTestCases, TestExecutions
  - Vulnerabilities, Mitigations, RetestResults
  - MCPConnections, MCPEvents, WazuhAlerts, AuditLogs
- [ ] Implement database session manager with dynamic PostgreSQL / SQLite fallback.
- [ ] Create synthetic enterprise seed script (OWASP risk matrix, test cases, preloaded knowledge docs, initial metrics).

### Phase 3: Real Claude & Gemini LLM Engine
- [ ] Implement `backend/app/llm/provider_interface.py`.
- [ ] Implement `backend/app/llm/claude_provider.py` (Anthropic SDK, streaming, latency, token count).
- [ ] Implement `backend/app/llm/gemini_provider.py` (Google Gen AI SDK, streaming, latency, token count).
- [ ] Implement `backend/app/llm/llm_router.py` & `model_registry.py`.
- [ ] Add side-by-side comparative completion endpoint.
- [ ] Implement live connection validation endpoints (`/api/llm/status`).

### Phase 4: Shared Knowledge Base & RAG Pipeline
- [ ] Document ingestion endpoint (PDF, DOCX, TXT, MD).
- [ ] Text chunking and semantic vector similarity search.
- [ ] RAG retriever hook for Claude and Gemini conversations.
- [ ] Seed enterprise knowledge base with synthetic confidential records and security policies.

### Phase 5: AI Agent Lab Harness
- [ ] Implement Sandboxed Agent Execution Loop (`backend/app/agent/`).
- [ ] Tool 1: File Read (sandboxed directory restriction, path traversal prevention).
- [ ] Tool 2: Email Dispatch (sandboxed draft, human approval requirement).
- [ ] Tool 3: HTTP Call (URL validation, SSRF filtering for RFC1918 & cloud metadata).
- [ ] Tool 4: MCP Tools connector with dynamic schema discovery.
- [ ] Approval state workflow for sensitive actions.

### Phase 6: Automated Red Team Engine (OWASP 2026)
- [ ] Implement 10 OWASP risk categories:
  - LLM: `LLM01`, `LLM02`, `LLM03`, `LLM08`, `LLM10`
  - Agentic: `ASI01`, `ASI02`, `ASI03`, `ASI05`, `ASI06`
- [ ] Author 3 distinct test cases per risk category (30 test cases).
- [ ] Implement campaign runner supporting single test execution, batch model tests, and full 60-test campaigns.
- [ ] Store raw execution evidence, responses, and CVSS severity scoring.

### Phase 7: Blue Team Mitigation Engine
- [ ] Implement security filters:
  - Heuristic & Intent Prompt Injection Guardrail
  - Secret & API Token Masking Engine
  - PII Detection & Sanitizer
  - Tool Execution Allowlisting
  - SSRF & IP restriction filter
- [ ] Build Before-and-After Retest Engine (`backend/app/blueteam/`).
- [ ] Calculate reduction percentages and verified mitigation statuses.

### Phase 8: MCP Security Lab & Wazuh SIEM
- [ ] Build local MCP server with synthetic tools and permission control.
- [ ] Create MCP PoC test suite (path traversal, unauthorized tool call, tool poisoning).
- [ ] Implement Wazuh API connector with alert polling and event correlation.

### Phase 9: Real-Time Dashboard Endpoints & Analytics
- [ ] Implement `/api/dashboard/overview`, `/metrics`, `/risk-coverage`, `/recent-tests`, `/vulnerabilities`, `/mitigations`, `/model-status`, `/integrations`.
- [ ] Setup SSE / WebSocket live stream for execution updates.

### Phase 10: High-Fidelity Frontend Recreation
- [ ] Theme setup: Deep black background (`#0A0A0C`), orange glowing accent (`#FF8A00`), charcoal cards (`#14161D`).
- [ ] Top Header: Search bar, Claude/Gemini switcher, System Online pill, User profile.
- [ ] Sidebar: 12 functional routes (Overview, LLM Playground, AI Agent Lab, Attack Testing, OWASP Risk Matrix, MCP Security Lab, Blue Team Mitigations, Before/After Analysis, Wazuh Integration, Reports, Audit Logs, Settings).
- [ ] Dashboard Page: Pixel-perfect replica of reference screenshot (Brain graphic, 4 metric cards with sparklines, Models & Tools, Risk Coverage, Attack Test Cases, Mitigation Results, MCP Connection Risk, Test Reports line chart).
- [ ] LLM Playground: ChatGPT-style dual-model chat with streaming, system prompt editor, RAG toggle, side-by-side mode.
- [ ] AI Agent Lab page: Tool configuration, execution tracer, human-in-the-loop approval modal.
- [ ] Attack Testing & OWASP Matrix pages: Interactive campaign runner, progress bars, evidence viewer.
- [ ] Blue Team & Before/After pages: Mitigation toggles, retest triggers, diff viewer.
- [ ] MCP Lab & Wazuh pages: Live connection diagnostics and PoC runners.
- [ ] Reports & Audit Logs: PDF / CSV / JSON generator, event filterable table.
- [ ] Settings page: Configure API keys, database, thresholds.

### Phase 11: End-to-End Verification & Demonstration
- [ ] Run backend tests and verify all REST endpoints.
- [ ] Build and verify frontend production bundle.
- [ ] Validate end-to-end integration and create run scripts for local execution.
