# Development & Security Rules
## AI SECURITY FASTER – AI Red Teaming & Blue Teaming Operations Center

### 1. Security & Red Teaming Architecture Rules
1. **Synthetic & Controlled Testing Only**:
   - All red teaming payloads must execute against controlled mock environments or strictly synthetic targets (e.g. synthetic company canary records, isolated sandbox directories).
   - Never direct outbound network requests or payloads to external real-world targets or private networks.
2. **Zero Client-Side Secret Exposure**:
   - Anthropic API keys (`ANTHROPIC_API_KEY`) and Google Gemini API keys (`GEMINI_API_KEY`) must strictly reside on the backend server.
   - Frontend requests must only interact with `/api/llm/*` proxy endpoints.
3. **Verified Mitigation Retest Policy**:
   - A vulnerability status cannot be changed to `MITIGATED` manually or hypothetically.
   - The platform must re-run the exact adversarial prompt payload against the model with active mitigations engaged and verify that the security check blocked or sanitized the response.
4. **Authentic Metric Reporting**:
   - Do not display fabricated alerts or fake connection statuses.
   - If an API key is missing or an integration (e.g., Wazuh, MCP) is unreachable, the system must clearly display `Unconfigured` or `Disconnected`.

### 2. Code Quality & Standards
1. **Backend (Python / FastAPI)**:
   - Type hints throughout using Pydantic v2 and Python 3.10+ typing.
   - Asynchronous endpoints (`async def`) for non-blocking I/O, streaming LLM completions, and background task dispatch.
   - SQLAlchemy 2.0 declarative models with UUID primary keys and standard timestamps (`created_at`, `updated_at`).
   - Clean modular division: `api`, `core`, `database`, `models`, `schemas`, `llm`, `rag`, `agent`, `redteam`, `blueteam`, `mcp`, `wazuh`, `reporting`.
2. **Frontend (React / TypeScript / Vite)**:
   - Strict TypeScript checking; zero `any` where avoidable.
   - Component styling via Tailwind CSS adhering strictly to the `#FF8A00` orange accent and `#0A0A0C` charcoal dark mode palette.
   - Reusable UI primitives leveraging Lucide React icons and Recharts data visualizations.
   - Global state / contexts for selected LLM model, active campaign status, and notifications.

### 3. Verification & Acceptance Criteria
- Every route defined in the specification must be implemented and return valid JSON or stream chunks.
- All 10 OWASP risk categories (5 LLM, 5 Agentic) must have at least 3 concrete test cases each (30 tests total).
- Live execution support for both Claude and Gemini with side-by-side comparison.
