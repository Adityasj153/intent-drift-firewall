from database.database import Database


class AuditLogger:
    """
    Stores completed pipeline executions in the audit database.
    """

    def __init__(self):
        self.db = Database()

    def log(self, context):
        """
        Persist a Context object into the database.
        """

        conn = self.db.connect()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO requests (

                request_id,
                timestamp,
                query,
                selected_tool,
                risk_score,
                severity,
                policy,
                execution_time,
                status,
                error

            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                context.request_id,
                context.timestamp,
                context.query,
                context.selected_tool,

                context.risk.get("risk_score")
                if context.risk else None,

                context.risk.get("severity")
                if context.risk else None,

                context.policy.get("action")
                if context.policy else None,

                context.execution.get("duration_ms")
                if context.execution else None,

                context.execution.get("status")
                if context.execution else None,

                context.execution.get("error")
                if context.execution else None,
            )
        )

        conn.commit()
        conn.close()