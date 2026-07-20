from datetime import datetime
import uuid


class Context:
    """
    Shared object that flows through the entire pipeline.

    Every component reads from and writes to this object.
    """

    def __init__(self, query: str):

        # ---------- Request Metadata ----------
        self.request_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow().isoformat()

        # ---------- User Input ----------
        self.query = query                   # Original query
        self.normalized_query = query        # Query after preprocessing

        # ---------- Routing ----------
        self.selected_tool = None

        # ---------- Firewall ----------
        self.drift = None
        self.prompt_injection = None

        # ---------- Risk ----------
        self.risk = None

        # ---------- Decision ----------
        self.policy = None

        # ---------- Execution ----------
        self.execution = None

        # ---------- Output ----------
        self.result = None

    def to_dict(self):

        return {
            "request_id": self.request_id,
            "timestamp": self.timestamp,
            "query": self.query,
            "normalized_query": self.normalized_query,
            "selected_tool": self.selected_tool,
            "drift": self.drift,
            "prompt_injection": self.prompt_injection,
            "risk": self.risk,
            "policy": self.policy,
            "execution": self.execution,
            "result": self.result,
        }