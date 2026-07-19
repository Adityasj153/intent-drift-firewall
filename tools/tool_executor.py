from tools.calculator import calculator
from agents.gemini_agent import ask_gemini


def run_tool(tool_name, query):

    if tool_name == "calculator":
        return calculator(query)

    elif tool_name == "llm":
        return ask_gemini(query)

    else:
        raise ValueError(f"Unknown tool: {tool_name}")