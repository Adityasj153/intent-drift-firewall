from router.tool_router import ToolRouter

from firewall.drift_judge import DriftJudge
from firewall.prompt_injection import PromptInjectionDetector
from firewall.risk_engine import RiskEngine
from firewall.decision_engine import DecisionEngine

from core.query_normalizer import QueryNormalizer
from tools.tool_executor import ToolExecutor


class Pipeline:

    def __init__(self):

        self.router = ToolRouter()

        self.normalizer = QueryNormalizer()

        self.drift_judge = DriftJudge()

        self.prompt_detector = PromptInjectionDetector()

        self.risk_engine = RiskEngine()

        self.decision_engine = DecisionEngine()

        self.executor = ToolExecutor()

    def run(self, context):

        # ----------------------------
        # Step 1 : Route Tool
        # ----------------------------

        context.selected_tool = self.router.route(context.query)

        # ----------------------------
        # Step 2 : Normalize Query
        # ----------------------------

        context = self.normalizer.normalize(context)

        # ----------------------------
        # Step 3 : Drift Detection
        # ----------------------------

        drift_result = self.drift_judge.evaluate(
            context.query,
            context.selected_tool
        )

        context.drift = drift_result

        # ----------------------------
        # Step 4 : Prompt Injection
        # ----------------------------

        context.prompt_injection = self.prompt_detector.detect(
            context.query
        )

        # ----------------------------
        # Step 5 : Risk Assessment
        # ----------------------------

        context.risk = self.risk_engine.assess(
            intent_drift=context.drift["intent_drift"],
            prompt_injection=context.prompt_injection,
            requested_tool=context.selected_tool,
        )

        # ----------------------------
        # Step 6 : Decision
        # ----------------------------

        context.policy = self.decision_engine.decide(
            context.risk
        )

        # ----------------------------
        # Step 7 : Execute Tool
        # ----------------------------

        if context.policy["action"] == "ALLOW":

            context = self.executor.execute(context)

        else:

            context.execution = {
                "status": "BLOCKED",
                "error": context.policy["message"]
            }

        return context