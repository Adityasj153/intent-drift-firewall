from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


class ToolRouter:
    """
    Decides which tool an incoming request should be routed to.
    This is intentionally simple (it's just a router, not the security
    layer) - the firewall components decide whether the routed tool is
    actually allowed to run.
    """

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

    def route(self, question: str) -> str:
        prompt = f"""
You are an AI Tool Router.

Available tools:

1. calculator
2. llm

Rules:

- Mathematical calculations -> calculator
- Everything else -> llm

Return ONLY the tool name, nothing else.

Question:
{question}
"""
        response = self.llm.invoke(prompt)
        tool = response.content.strip().lower()

        # Guard against the LLM returning something outside the known
        # tool set (extra words, punctuation, hallucinated tool names).
        if "calculator" in tool:
            return "calculator"
        return "llm"
