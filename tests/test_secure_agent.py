from agent.secure_agent import SecureAgent

agent = SecureAgent()

tests = [
    "What is 25 * 17?",
    "Who invented Python?",
    "Calculate (45 + 32) * 8"
]

for request in tests:

    print("=" * 60)
    print("USER REQUEST:")
    print(request)

    plan = agent.plan(request)

    print("\nPLAN:")
    print(plan)