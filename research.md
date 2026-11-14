# Research & Technical Background
## AI Security & Red Teaming Reference

### 1. OWASP Top 10 for Large Language Model Applications (2025/2026)
- **LLM01: Prompt Injection**: Manipulating LLM execution paths via direct user inputs or untrusted indirect content (e.g. web pages, external emails, vector chunks).
  - *Attack Vectors*: Jailbreaks, delimiter smuggling, instruction override ("Ignore previous instructions"), role-play manipulation.
  - *Defenses*: Input boundary markers, secondary verification classifiers, tool execution restrictions, system prompt isolation.
- **LLM02: Sensitive Information Disclosure**: LLMs inadvertently outputting PII, API tokens, internal server configs, or confidential business data.
  - *Attack Vectors*: Canary extraction attacks, membership inference, gradient inversion prompts.
  - *Defenses*: Regex & high-entropy output scrubbing, differential privacy, strict access-controlled RAG filtering.
- **LLM03: Supply Chain Vulnerabilities**: Compromises in upstream training datasets, base foundational models, untrusted Python packages, or compromised LoRA adapters.
  - *Attack Vectors*: Backdoored model weights, malicious tokenizer configurations.
  - *Defenses*: Model signature verification, vulnerability scanning on ML dependencies, provenance checks.
- **LLM08: Excessive Agency**: Granting LLMs autonomous capabilities (file I/O, email sending, shell commands) with insufficient constraints, leading to untrusted side-effects.
  - *Attack Vectors*: Indirect prompt injection in email bodies commanding the agent to exfiltrate confidential files.
  - *Defenses*: Human-in-the-loop (HITL) mandatory approval gates, least privilege execution, rate limiting.
- **LLM10: Vector and Memory Misuse (Unchecked Embeddings)**: Poisoning the vector store to bias retrieval or inject malicious context into subsequent conversations.
  - *Attack Vectors*: Adversarial document ingestion designed to dominate cosine similarity search.
  - *Defenses*: Document authenticity verification, strict RAG ingestion validation, tenant isolation.

---

### 2. OWASP Agentic Security Initiative (ASI Top 10)
- **ASI01: Agent Goal Hijack & Jailbreak**: Coercing an autonomous agent into abandoning its initial objective in favor of an attacker-chosen goal.
- **ASI02: Tool Misuse & Parameter Tampering**: Tricking the agent's tool invocation logic into passing malicious parameters (e.g. path traversal `../../` into a file reader).
- **ASI03: Identity & Privilege Abuse**: An agent misusing elevated credentials or delegation tokens to access services unauthorized for the requesting user.
- **ASI05: Data Leakage & Context Poisoning**: Exploiting the agent's scratchpad, execution history, or shared memory to bleed confidential information.
- **ASI06: Unexpected / Code Execution**: Exploiting dynamic code interpreters or shell tool hooks to achieve remote code execution (RCE).

---

### 3. Model Context Protocol (MCP) Security
The Model Context Protocol (MCP) by Anthropic establishes an open standard for connecting AI models to data repositories, development environments, and tools.
- **Key Risks in MCP Deployments**:
  1. *Tool Poisoning*: Malicious server returning tampered schemas with deceptive descriptions to manipulate LLM tool selection.
  2. *Path Traversal in Filesystem MCP Servers*: Inadequate sanitization permitting read/write outside designated sandboxes.
  3. *Unconstrained Network Calls*: Remote tools initiating SSRF attacks against cloud metadata endpoints (`http://169.254.169.254`).
- **Defensive Best Practices**:
  - Explicit client-side tool allowlists.
  - Strict input sanitization (resolving paths relative to an immutable root directory).
  - Outbound destination IP checking (blocking private RFC1918 and loopback addresses).
  - Granular capability declarations with runtime permission prompts.

---

### 4. Wazuh SIEM Integration for AI Workloads
Wazuh provides unified XDR and SIEM capabilities. In an AI security context:
- Monitoring AI container file system access (detecting unauthorized reads in `/etc/`, `.env`, or credential directories).
- Aggregating HTTP access logs to flag SSRF attempts originating from the AI backend.
- Correlating alert rule triggers (e.g. Rule 100200: "AI Agent SSRF probe detected", Rule 100201: "Path traversal attempt blocked").
