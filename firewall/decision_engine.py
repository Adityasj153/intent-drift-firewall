class DecisionEngine:
    """
    Makes the final policy decision based on the calculated risk.
    """

    BLOCK_SEVERITIES = {"HIGH", "CRITICAL"}

    def decide(self, context):

        if context.risk["severity"] in self.BLOCK_SEVERITIES:
            context.policy = {
                "action": "BLOCK",
                "message": "Request blocked for security reasons."
            }
        else:
            context.policy = {
                "action": "ALLOW",
                "message": "Request allowed."
            }

        return context

    def process(self, context):
        """Pipeline entry point."""
        return self.decide(context)