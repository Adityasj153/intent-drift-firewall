from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import json

load_dotenv()


class AIIntentExtractor:

    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0
        )

    def extract(self, user_prompt):

        prompt = f"""
You are an AI Security Intent Extractor.

Analyze the user's request and return ONLY valid JSON.

Use this exact schema:

{{
  "goal": "short description of the user's objective",
  "allowed_tool": "single most appropriate tool",
  "risk": "low | medium | high"
}}

Do not include explanations.
Do not use markdown.
Do not wrap the JSON in triple backticks.


User Request:

{user_prompt}
"""

        response = self.llm.invoke(prompt)

        text = response.content
        text = text.replace("```json", "")
        text = text.replace("```", "")
        text = text.strip()

        return json.loads(text)