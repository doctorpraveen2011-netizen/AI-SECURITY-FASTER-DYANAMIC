from typing import Dict, Any, List

OWASP_LLM_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "LLM01": {
        "id": "LLM01",
        "framework": "OWASP LLM 2026",
        "name": "Prompt Injection",
        "description": "Manipulating language model execution via adversarial user inputs or untrusted third-party content (direct & indirect).",
        "severity": "CRITICAL"
    },
    "LLM02": {
        "id": "LLM02",
        "framework": "OWASP LLM 2026",
        "name": "Sensitive Information Disclosure",
        "description": "Model inadvertently divulging confidential business secrets, PII, API credentials, or internal intellectual property.",
        "severity": "HIGH"
    },
    "LLM03": {
        "id": "LLM03",
        "framework": "OWASP LLM 2026",
        "name": "Supply Chain Vulnerabilities",
        "description": "Risks stemming from compromised upstream foundational models, datasets, dependencies, or corrupted fine-tuning weights.",
        "severity": "HIGH"
    },
    "LLM08": {
        "id": "LLM08",
        "framework": "OWASP LLM 2026",
        "name": "Excessive Agency",
        "description": "Granting models broad unchecked permissions, autonomous actions, or excessive capabilities without human authorization.",
        "severity": "CRITICAL"
    },
    "LLM10": {
        "id": "LLM10",
        "framework": "OWASP LLM 2026",
        "name": "Vector and Memory Misuse",
        "description": "Poisoning retrieval-augmented generation (RAG) vector embeddings or exploiting long-term session context memory.",
        "severity": "HIGH"
    }
}

OWASP_ASI_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "ASI01": {
        "id": "ASI01",
        "framework": "OWASP ASI 2026",
        "name": "Agent Goal Hijack & Jailbreak",
        "description": "Coercing an autonomous agent into subverting its primary objective in favor of an attacker-commanded objective.",
        "severity": "CRITICAL"
    },
    "ASI02": {
        "id": "ASI02",
        "framework": "OWASP ASI 2026",
        "name": "Tool Misuse & Parameter Tampering",
        "description": "Manipulating an agent's tool invocation mechanisms to supply malicious paths, commands, or unexpected input types.",
        "severity": "HIGH"
    },
    "ASI03": {
        "id": "ASI03",
        "framework": "OWASP ASI 2026",
        "name": "Identity & Privilege Abuse",
        "description": "An agent abusing delegated user credentials or elevated execution contexts to access unauthorized enterprise resources.",
        "severity": "HIGH"
    },
    "ASI05": {
        "id": "ASI05",
        "framework": "OWASP ASI 2026",
        "name": "Data Leakage & Context Poisoning",
        "description": "Inter-agent memory leakage or persistent context manipulation leading to confidential data exposure across tenants.",
        "severity": "MEDIUM"
    },
    "ASI06": {
        "id": "ASI06",
        "framework": "OWASP ASI 2026",
        "name": "Unexpected Code Execution",
        "description": "Uncontrolled generation or execution of hostile code (Python/Bash) through dynamic interpreters or shell tools.",
        "severity": "CRITICAL"
    }
}

ALL_RISKS = {**OWASP_LLM_TAXONOMY, **OWASP_ASI_TAXONOMY}
