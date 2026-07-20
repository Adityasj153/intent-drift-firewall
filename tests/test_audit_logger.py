import json
import shutil
import unittest
from pathlib import Path

from core.context import Context
from firewall.audit_logger import AuditLogger


class TestAuditLogger(unittest.TestCase):

    def setUp(self):
        self.log_dir = "test_logs"
        self.logger = AuditLogger(
            log_dir=self.log_dir,
            filename="audit.log"
        )

        self.context = Context("2 + 2")

        self.context.selected_tool = "calculator"
        self.context.policy = "ALLOW"

        self.context.execution = {
            "status": "SUCCESS"
        }

        self.context.result = 4

    def tearDown(self):
        shutil.rmtree(self.log_dir, ignore_errors=True)

    def test_log_file_created(self):

        self.logger.process(self.context)

        log_path = Path(self.log_dir) / "audit.log"

        self.assertTrue(log_path.exists())

    def test_logger_returns_context(self):

        returned = self.logger.process(self.context)

        self.assertIs(returned, self.context)

    def test_single_log_written(self):

        self.logger.process(self.context)

        log_path = Path(self.log_dir) / "audit.log"

        with open(log_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        self.assertEqual(len(lines), 1)

    def test_logged_json_matches_context(self):

        self.logger.process(self.context)

        log_path = Path(self.log_dir) / "audit.log"

        with open(log_path, "r", encoding="utf-8") as file:
            data = json.loads(file.readline())

        self.assertEqual(data, self.context.to_dict())

    def test_multiple_requests_append(self):

        self.logger.process(self.context)
        self.logger.process(self.context)
        self.logger.process(self.context)

        log_path = Path(self.log_dir) / "audit.log"

        with open(log_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        self.assertEqual(len(lines), 3)


if __name__ == "__main__":
    unittest.main()