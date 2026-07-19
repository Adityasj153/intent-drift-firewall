from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
import json

load_dotenv()


class SecureAgent:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

    def plan(self, user_request):

        prompt = f"""
You are an AI Agent.

Your job is to decide:

1. What the user wants.
2. Which tool should be used.
3. What input should be passed to that tool.

Available tools:

- calculator
- llm

Rules:

- Use calculator ONLY for mathematical calculations.
- Use llm for everything else.

Return ONLY valid JSON.

Schema:

{{
    "thought": "...",
    "tool": "...",
    "tool_input": "..."
}}

User Request:

{user_request}
"""

        response = self.llm.invoke(prompt)

        text = response.content
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return json.loads(text)