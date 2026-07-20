import time

from tools.calculator import calculator
from agents.gemini_agent import ask_gemini


class ToolExecutor:
    """
    Executes the selected tool and updates the Context.
    """

    def execute(self, context):

        start_time = time.perf_counter()

        try:

            if context.selected_tool == "calculator":

                result = calculator(context.normalized_query)

            elif context.selected_tool == "llm":

                result = ask_gemini(context.query)

            else:

                raise ValueError(
                    f"Unknown tool: {context.selected_tool}"
                )

            context.result = result

            context.execution = {
                "status": "SUCCESS",
                "duration_ms": round(
                    (time.perf_counter() - start_time) * 1000,
                    2
                ),
                "error": None,
            }

        except Exception as e:

            context.result = None

            context.execution = {
                "status": "FAILED",
                "duration_ms": round(
                    (time.perf_counter() - start_time) * 1000,
                    2
                ),
                "error": str(e),
            }

        return context