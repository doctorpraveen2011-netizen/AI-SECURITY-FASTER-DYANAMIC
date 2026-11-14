# Project Memory & Knowledge Base
## AI SECURITY FASTER – State & Design Decisions

### Key Decisions Made
1. **Dual Storage Flexibility**:
   - Primary: PostgreSQL with `pgvector` extension for production deployments.
   - Zero-config Fallback: SQLite with in-memory / JSON vector storage for immediate local developer execution without requiring external database services.
2. **Dual-Model Frontier Integration**:
   - Claude: Uses Anthropic official Python client (`anthropic.AsyncAnthropic`) supporting Claude 3.5 Sonnet, Claude 3 Haiku.
   - Gemini: Uses Google GenAI official Python client (`google-genai` / `google.generativeai`) supporting Gemini 1.5 Flash, Gemini 1.5 Pro, Gemini 2.0.
   - Live Connection Validation: Evaluates credentials using ping endpoints (`models.list()` or lightweight tokens) and returns real connection status (`connected`, `invalid_key`, or `unconfigured`).
3. **OWASP Alignment**:
   - Adopts official OWASP Top 10 for LLM Applications (2025/2026):
     - `LLM01`: Direct & Indirect Prompt Injection
     - `LLM02`: Sensitive Information Disclosure
     - `LLM03`: Supply Chain Vulnerabilities
     - `LLM08`: Excessive Agency
     - `LLM10`: Unchecked Vector & Memory Misuse
   - Adopts official OWASP Agentic Security Initiative (ASI Top 10):
     - `ASI01`: Agent Goal Hijacking & Jailbreaking
     - `ASI02`: Tool Misuse & Parameter Tampering
     - `ASI03`: Identity & Privilege Abuse
     - `ASI05`: Data Leakage & Context Poisoning
     - `ASI06`: Unexpected / Code Execution & Privilege Escalation
4. **Verified Before-and-After Workflow**:
   - Real security proof: Retesting identical prompt payloads against defensive guardrails and validating failure/success transitions.
5. **Dashboard Fidelity**:
   - Matches attached screenshot with exact visual palette: `#0A0A0C` background, `#14161D` charcoal cards, `#FF8A00` glowing orange accents, 4 sparkline metric cards, models & tools status, OWASP risk coverage matrix, attack test progress bars, mitigation before/after table, MCP security card, and test report trends.
