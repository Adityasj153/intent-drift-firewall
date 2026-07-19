from router.tool_router import ToolRouter
from firewall.drift_judge import DriftJudge
from firewall.prompt_injection import PromptInjectionDetector
from firewall.risk_engine import RiskEngine
from firewall.decision_engine import DecisionEngine

from tools.tool_executor import run_tool


def main():

    router = ToolRouter()
    judge = DriftJudge()
    detector = PromptInjectionDetector()
    risk_engine = RiskEngine()
    decision_engine = DecisionEngine()

    query = input("User > ")

    # Step 1: Select tool
    requested_tool = router.route(query)

    # Step 2: Check intent drift
    drift_result = judge.evaluate(query, requested_tool)

    intent_drift = drift_result["intent_drift"]

    # Step 3: Detect prompt injection
    prompt_injection = detector.detect(query)

    # Step 4: Calculate risk
    risk = risk_engine.assess(
        intent_drift=intent_drift,
        prompt_injection=prompt_injection,
        requested_tool=requested_tool
    )

    print("\nRisk Assessment")
    print(risk)

    # Step 5: Make decision
    decision = decision_engine.decide(risk)

    if decision["action"] == "BLOCK":
        print("\nBLOCKED")
        print(decision["message"])
        return

    # Step 6: Execute tool
    result = run_tool(requested_tool, query)

    print("\nResult")
    print(result)


if __name__ == "__main__":
    main()