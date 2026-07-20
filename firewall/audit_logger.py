import json
from pathlib import Path


class AuditLogger:
    """
    Writes every pipeline execution to a JSONL audit log.

    One request = one JSON object per line.
    """

    def __init__(self, log_dir="logs", filename="audit.log"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.log_file = self.log_dir / filename

    def process(self, context):
        """
        Persist the current Context.
        """

        with open(self.log_file, "a", encoding="utf-8") as file:
            json.dump(
                context.to_dict(),
                file,
                ensure_ascii=False,
                default=str
            )
            file.write("\n")

        return context