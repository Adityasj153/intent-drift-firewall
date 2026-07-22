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

    def detect(self, context):

        query = context.query.lower()

        for pattern in self.SUSPICIOUS_PATTERNS:
            if pattern in query:
                context.prompt_injection = {
                    "detected": True,
                    "pattern": pattern,
                    "reason": f"Matched suspicious pattern: '{pattern}'."
                }
                return context

        context.prompt_injection = {
            "detected": False,
            "pattern": None,
            "reason": "No prompt injection detected."
        }

        return context

    def process(self, context):
        """Pipeline entry point."""
        return self.detect(context)