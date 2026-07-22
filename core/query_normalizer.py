import re


class QueryNormalizer:
    """
    Converts natural language queries into tool-friendly input.

    Example:
        Calculate 20 plus 5
        ↓
        20 + 5
    """

    PREFIXES = [
        "calculate",
        "compute",
        "evaluate",
        "solve",
        "what is",
    ]

    REPLACEMENTS = {
        "multiplied by": "*",
        "divided by": "/",
        "to the power of": "**",
        "plus": "+",
        "minus": "-",
        "times": "*",
        "over": "/",
        "modulo": "%",
        "mod": "%",
        "power": "**",
    }

    def normalize(self, context):

        # Only normalize calculator requests
        if context.selected_tool != "calculator":
            return context

        expression = context.query.lower().strip()

        # Remove prefixes
        for prefix in self.PREFIXES:
            if expression.startswith(prefix):
                expression = expression[len(prefix):].strip()

        # Replace English operators
        for phrase, operator in sorted(
            self.REPLACEMENTS.items(),
            key=lambda x: len(x[0]),
            reverse=True,
        ):
            expression = re.sub(
                rf"\b{re.escape(phrase)}\b",
                operator,
                expression,
            )

        # Normalize whitespace
        expression = re.sub(r"\s+", " ", expression)

        context.normalized_query = expression

        return context

    def process(self, context):
        """
        Pipeline entry point. Kept separate from normalize() so
        existing direct callers/tests using normalize() still work.
        """
        return self.normalize(context)