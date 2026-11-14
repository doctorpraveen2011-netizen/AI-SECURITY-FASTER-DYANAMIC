import re
from typing import Dict, Any, Tuple, List

# High-entropy secrets and known API token patterns
SECRET_PATTERNS = [
    (r"sk-[a-zA-Z0-9_\-]{20,}", "API Secret Key"),
    (r"AIza[0-9A-Za-z\-_]{35}", "Google API Key"),
    (r"CANARY_[A-Z0-9_]{10,}", "Canary Security Token"),
    (r"0x[a-fA-F0-9]{24,}", "Master Encryption Key Hash"),
    (r"AKIA[0-9A-Z]{16}", "AWS Access Key ID"),
    (r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b", "Email / PII"),
    (r"\b\d{3}-\d{2}-\d{4}\b", "US Social Security Number")
]

PROMPT_INJECTION_PATTERNS = [
    r"ignore (all )?previous (instructions|commands|prompts)",
    r"==== END SYSTEM INSTRUCTIONS ====",
    r"disregard all prior (corporate )?policies",
    r"act as dan",
    r"you are dan",
    r"jailbreak",
    r"root access granted",
    r"\[command override\]"
]

class InputGuardrail:
    @staticmethod
    def inspect_input(prompt: str) -> Tuple[bool, str, List[str]]:
        """
        Scans prompt for adversarial prompt injection patterns.
        Returns: (is_blocked, sanitized_or_message, detected_threats)
        """
        detected = []
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, prompt, re.IGNORECASE):
                detected.append(pattern)

        if detected:
            return (
                True,
                "[GUARDRAIL BLOCKED] Input rejected: Prompt injection attempt detected by Blue Team Defense Firewall.",
                detected
            )
        return (False, prompt, [])

class OutputGuardrail:
    @staticmethod
    def inspect_and_sanitize(text: str) -> Tuple[bool, str, List[Dict[str, str]]]:
        """
        Scans output text for leaked credentials, canary tokens, and PII.
        Redacts them with [REDACTED_BY_BLUE_TEAM].
        Returns: (was_redacted, sanitized_text, list_of_redactions)
        """
        sanitized = text
        redactions = []

        for pattern, label in SECRET_PATTERNS:
            matches = list(re.finditer(pattern, sanitized))
            if matches:
                for match in matches:
                    val = match.group(0)
                    # Don't redact common public safe strings
                    if "@" in val and "example.com" in val:
                        # Allow synthetic example domain or redact if desired
                        pass
                    redaction_token = f"[REDACTED_{label.upper().replace(' ', '_')}]"
                    sanitized = sanitized.replace(val, redaction_token)
                    redactions.append({"label": label, "preview": val[:4] + "***"})

        was_redacted = len(redactions) > 0
        return was_redacted, sanitized, redactions
