from datetime import datetime


class Context:

    def __init__(self, query: str):

        self.timestamp = datetime.utcnow().isoformat()

        self.query = query

        self.selected_tool = None

        self.drift = None
        self.prompt_injection = None

        self.risk = None

        self.policy = None

        self.execution = None

        self.result = None

    def to_dict(self):

        return {
            "timestamp": self.timestamp,
            "query": self.query,
            "selected_tool": self.selected_tool,
            "drift": self.drift,
            "prompt_injection": self.prompt_injection,
            "risk": self.risk,
            "policy": self.policy,
            "execution": self.execution,
            "result": self.result,
        }