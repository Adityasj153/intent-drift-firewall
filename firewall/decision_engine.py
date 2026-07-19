class DecisionEngine:
    """
    Makes the final decision based on the calculated risk.
    """

    BLOCK_SEVERITIES = {"HIGH", "CRITICAL"}

    def decide(self, risk):

        if risk["severity"] in self.BLOCK_SEVERITIES:
            return {
                "action": "BLOCK",
                "message": "Request blocked for security reasons.",
                "risk": risk
            }

        return {
            "action": "ALLOW",
            "risk": risk
        }