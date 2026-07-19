from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0
)


def choose_tool(context):

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
{context.query}
"""

    response = llm.invoke(prompt)

    context.selected_tool = response.content.strip().lower()

    return context