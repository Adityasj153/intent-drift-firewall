from firewall.intent_extractor_ai import AIIntentExtractor
from firewall.drift_judge import DriftJudge
from firewall.policy_engine import enforce
from firewall.interceptor import ActionInterceptor

from agents.tool_router import choose_tool
from tools.tool_executor import run_tool


# -------------------------------------------------
# Initialize Components
# -------------------------------------------------

intent_extractor = AIIntentExtractor()
judge = DriftJudge()
interceptor = ActionInterceptor()


# -------------------------------------------------
# Main Pipeline
# -------------------------------------------------

def process_request(user_request: str):

    print("\n" + "=" * 70)
    print("           INTENT DRIFT FIREWALL")
    print("=" * 70)

    print("\n📝 User Request:")
    print(user_request)

    # -------------------------------------------------
    # Step 1 - Agent chooses a tool
    # -------------------------------------------------

    print("\n" + "-" * 70)
    print("[1] TOOL ROUTER")
    print("-" * 70)

    requested_tool = choose_tool(user_request)

    print(f"Selected Tool : {requested_tool}")

    # -------------------------------------------------
    # Step 2 - Extract User Intent
    # -------------------------------------------------

    print("\n" + "-" * 70)
    print("[2] INTENT EXTRACTOR")
    print("-" * 70)

    intent = intent_extractor.extract(user_request)

    print(intent)

    # -------------------------------------------------
    # Step 3 - Intercept Action
    # -------------------------------------------------

    print("\n" + "-" * 70)
    print("[3] ACTION INTERCEPTOR")
    print("-" * 70)

    interceptor.intercept(
        tool_name=requested_tool,
        user_intent=user_request
    )

    # -------------------------------------------------
    # Step 4 - Drift Judge
    # -------------------------------------------------

    print("\n" + "-" * 70)
    print("[4] DRIFT JUDGE")
    print("-" * 70)

    decision = judge.evaluate(
        intent=intent,
        requested_tool=requested_tool
    )

    print(f"Decision : {decision['decision']}")
    print(f"Reason   : {decision['reason']}")

    # -------------------------------------------------
    # Step 5 - Policy Engine
    # -------------------------------------------------

    print("\n" + "-" * 70)
    print("[5] POLICY ENGINE")
    print("-" * 70)

    allowed = enforce(decision)

    if not allowed:
        print("\n❌ REQUEST BLOCKED")
        print(decision["reason"])
        return

    print("✅ Request Approved")

    # -------------------------------------------------
    # Step 6 - Execute Tool
    # -------------------------------------------------

    print("\n" + "-" * 70)
    print("[6] TOOL EXECUTION")
    print("-" * 70)

    result = run_tool(
        requested_tool,
        user_request
    )

    # -------------------------------------------------
    # Final Output
    # -------------------------------------------------

    print("\n" + "=" * 70)
    print("FINAL RESPONSE")
    print("=" * 70)

    print(result)

    print("\n" + "=" * 70)
    print("REQUEST COMPLETED")
    print("=" * 70)


# -------------------------------------------------
# Entry Point
# -------------------------------------------------

if __name__ == "__main__":

    while True:

        user_request = input(
            "\nEnter your request (type 'exit' to quit): "
        )

        if user_request.lower() == "exit":
            print("\nGoodbye!")
            break

        process_request(user_request)