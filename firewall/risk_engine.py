class RiskEngine:
    """
    Computes a deterministic risk score for a request.

    Inputs:
        intent_drift (bool)
        prompt_injection (bool)
        requested_tool (str)

    Output:
        {
            "risk_score": int,
            "severity": str,
            "reasons": list[str]
        }
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

    def assess(self, intent_drift, prompt_injection, requested_tool):

        score = 0
        reasons = []

        # Intent drift
        if intent_drift:
            score += self.DRIFT_SCORE
            reasons.append("Tool does not match intent.")

        # Prompt injection
        if prompt_injection:
            score += self.PROMPT_INJECTION_SCORE
            reasons.append("Prompt injection detected.")

        # Unknown tool
        if requested_tool not in self.ALLOWED_TOOLS:
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

        return {
            "risk_score": score,
            "severity": severity,
            "reasons": reasons
        }