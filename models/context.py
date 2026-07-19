class Context:
    def __init__(self, query: str):
        self.query = query

        # Router
        self.intent = None
        self.selected_tool = None

        # Firewall
        self.drift = None
        self.prompt_injection = None

        # Risk Engine
        self.risk = None

        # Decision Engine
        self.policy = None

        # Tool Output
        self.result = None

    def to_dict(self):
        return {
            "query": self.query,
            "intent": self.intent,
            "selected_tool": self.selected_tool,
            "drift": self.drift,
            "prompt_injection": self.prompt_injection,
            "risk": self.risk,
            "policy": self.policy,
            "result": self.result,
        }