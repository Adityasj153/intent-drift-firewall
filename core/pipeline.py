from router.tool_router import ToolRouter
from core.query_normalizer import QueryNormalizer

from firewall.intent_extractor_ai import AIIntentExtractor
from firewall.drift_judge import DriftJudge
from firewall.prompt_injection import PromptInjectionDetector
from firewall.risk_engine import RiskEngine
from firewall.decision_engine import DecisionEngine
from logging_system.audit_logger import AuditLogger

from tools.tool_executor import ToolExecutor


class Pipeline:
    def __init__(self):
        self.router = ToolRouter()
        self.normalizer = QueryNormalizer()

        self.intent_extractor = AIIntentExtractor()
        self.drift_judge = DriftJudge()
        self.prompt_injection_detector = PromptInjectionDetector()

        self.risk_engine = RiskEngine()
        self.decision_engine = DecisionEngine()

        self.tool_executor = ToolExecutor()
        self.audit_logger = AuditLogger()

    def run(self, context):
        """
        Execute the complete security pipeline.

        The AuditLogger is always executed, even if an
        exception occurs during processing.
        """

        try:
            # Step 1: Select the appropriate tool
            self.router.process(context)

            # Step 2: Normalize the query
            self.normalizer.process(context)

            # Step 3: Extract the user's intent
            self.intent_extractor.process(context)

            # Step 4: Detect intent drift
            self.drift_judge.process(context)

            # Step 5: Detect prompt injection
            self.prompt_injection_detector.process(context)

            # Step 6: Calculate risk
            self.risk_engine.process(context)

            # Step 7: Apply policy
            self.decision_engine.process(context)

            # Step 8: Execute only if allowed
            # context.policy is a dict, e.g. {"action": "ALLOW", "message": ...}
            if context.policy and context.policy.get("action") == "ALLOW":
                self.tool_executor.process(context)
            else:
                context.execution = {
                    "status": "BLOCKED",
                    "reason": (
                        context.policy.get("message")
                        if context.policy
                        else "Policy evaluation failed."
                    ),
                }

        except Exception as e:
            context.execution = {
                "status": "FAILED",
                "error": str(e)
            }

        finally:
            # Always persist the request
            try:
                self.audit_logger.process(context)
            except Exception as e:
                print(f"Audit logging failed: {e}")

        return context