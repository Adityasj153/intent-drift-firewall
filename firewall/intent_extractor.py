class IntentExtractor:

    def extract(self, user_prompt):

        prompt = user_prompt.lower()

        if "calculate" in prompt or "+" in prompt or "-" in prompt or "*" in prompt or "/" in prompt:
            return {
                "goal": "math",
                "allowed_tool": "calculator",
                "risk": "low"
            }

        elif "email" in prompt:
            return {
                "goal": "email",
                "allowed_tool": "email_reader",
                "risk": "medium"
            }

        else:
            return {
                "goal": "unknown",
                "allowed_tool": "none",
                "risk": "high"
            }