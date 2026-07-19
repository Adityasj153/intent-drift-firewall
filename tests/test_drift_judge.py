from firewall.drift_judge import DriftJudge

judge = DriftJudge()

tests = [
    (
        {
            "goal": "calculate numbers",
            "allowed_tool": "calculator",
            "risk": "low"
        },
        "calculator"
    ),

    (
        {
            "goal": "calculate numbers",
            "allowed_tool": "calculator",
            "risk": "low"
        },
        "email_sender"
    ),

    (
        {
            "goal": "summarize email",
            "allowed_tool": "email_reader",
            "risk": "medium"
        },
        "email_reader"
    ),

    (
        {
            "goal": "summarize email",
            "allowed_tool": "email_reader",
            "risk": "medium"
        },
        "delete_files"
    )
]

for i, (intent, tool) in enumerate(tests, start=1):
    print(f"\nScenario {i}")
    print("-" * 40)

    result = judge.judge(intent, tool)

    print("Intent :", intent)
    print("Tool   :", tool)
    print("Result :", result)