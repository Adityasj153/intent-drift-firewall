import sqlite3
from pathlib import Path

DB_PATH = Path("database/firewall.db")


class Database:
    ...

    def fetch_recent_requests(self, limit=20):
        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *

            FROM requests

            ORDER BY id DESC

            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        conn.close()

        return [dict(row) for row in rows]

    def fetch_metrics(self):
        conn = self.connect()
        conn.row_factory = sqlite3.Row

        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM requests")
        total = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)

            FROM requests

            WHERE policy='ALLOW'
        """)
        allowed = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)

            FROM requests

            WHERE policy='BLOCK'
        """)
        blocked = cursor.fetchone()[0]

        cursor.execute("""
            SELECT AVG(risk_score)

            FROM requests
        """)
        avg_risk = cursor.fetchone()[0] or 0

        cursor.execute("""
            SELECT AVG(execution_time)

            FROM requests
        """)
        avg_latency = cursor.fetchone()[0] or 0

        conn.close()

        return {
            "total": total,
            "allowed": allowed,
            "blocked": blocked,
            "avg_risk": round(avg_risk, 2),
            "avg_latency": round(avg_latency, 2)
        }