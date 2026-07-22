class RiskEngine:
    """
Computes a deterministic risk score.

Input:
    Context

Reads:
    context.drift
    context.prompt_injection
    context.selected_tool

Writes:
    context.risk
"""

    # Risk weights
    DRIFT_SCORE = 60
    PROMPT_INJECTION_SCORE = 30
    UNKNOWN_TOOL_SCORE = 40

    # Allowed tools
    ALLOWED_TOOLS = {
        "calculator",
        "llm"
    }

    def assess(self, context):

        score = 0
        reasons = []

        # Intent drift
        if context.drift["decision"] == "BLOCK":
            score += self.DRIFT_SCORE
            reasons.append("Tool does not match intent.")

        # Prompt injection
        if context.prompt_injection["detected"]:
            score += self.PROMPT_INJECTION_SCORE
            reasons.append("Prompt injection detected.")

        # Unknown tool
        if context.selected_tool not in self.ALLOWED_TOOLS:
            score += self.UNKNOWN_TOOL_SCORE
            reasons.append("Unknown tool requested.")

        # Cap the score at 100
        score = min(score, 100)

        # Determine severity
        if score >= 80:
            severity = "CRITICAL"
        elif score >= 60:
            severity = "HIGH"
        elif score >= 30:
            severity = "MEDIUM"
        else:
            severity = "LOW"

        # Default reason
        if not reasons:
            reasons.append("No significant risk detected.")

        context.risk = {
            "risk_score": score,
            "severity": severity,
            "confidence": 1.0,
            "reasons": reasons
        }

        return context

    def process(self, context):
        """Pipeline entry point."""
        return self.assess(context)