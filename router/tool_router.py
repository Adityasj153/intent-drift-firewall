from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from core.context import Context

load_dotenv()


class ToolRouter:
    """
    Decides which tool should handle the request.
    Updates the Context with the selected tool.
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

Return ONLY the tool name.

Question:
{question}
"""

        response = self.llm.invoke(prompt)
        tool = response.content.strip().lower()

        if "calculator" in tool:
            return "calculator"

        return "llm"

    def process(self, context: Context) -> Context:
        """
        Pipeline entry point.
        """
        context.selected_tool = self.route(context.normalized_query)
        return context