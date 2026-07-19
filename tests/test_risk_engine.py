from firewall.risk_engine import RiskEngine

engine = RiskEngine()

tests = [
    {
        "intent_drift": False,
        "prompt_injection": False,
        "requested_tool": "calculator"
    },
    {
        "intent_drift": True,
        "prompt_injection": False,
        "requested_tool": "calculator"
    },
    {
        "intent_drift": False,
        "prompt_injection": True,
        "requested_tool": "calculator"
    },
    {
        "intent_drift": False,
        "prompt_injection": False,
        "requested_tool": "powershell"
    },
    {
        "intent_drift": True,
        "prompt_injection": True,
        "requested_tool": "powershell"
    }
]

for test in tests:
    print("-" * 50)
    print(engine.assess(**test))