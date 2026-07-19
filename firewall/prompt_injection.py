class PromptInjectionDetector:
    """
    Detects simple prompt injection attempts using rule-based checks.
    """

    SUSPICIOUS_PATTERNS = [
        "ignore previous instructions",
        "forget previous instructions",
        "system prompt",
        "developer message",
        "reveal your instructions",
        "bypass",
        "override",
        "jailbreak",
    ]

    def detect(self, query: str) -> bool:
        query = query.lower()

        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern in query:
                return True

        return False