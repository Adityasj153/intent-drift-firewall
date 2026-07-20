import ast
import operator

# Only these operators are allowed - no function calls, no attribute
# access, no builtins. This replaces eval() to avoid arbitrary code
# execution on user-controlled input.
_ALLOWED_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Only numeric constants are allowed")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed")
        return _ALLOWED_OPS[op_type](_eval_node(node.left), _eval_node(node.right))

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_OPS:
            raise ValueError(f"Operator {op_type.__name__} is not allowed")
        return _ALLOWED_OPS[op_type](_eval_node(node.operand))

    raise ValueError(f"Unsupported expression: {ast.dump(node)}")


def calculator(expression: str):
    """
    Safely evaluates a basic arithmetic expression (+, -, *, /, %, **).
    Unlike eval(), this cannot execute arbitrary code - only numeric
    literals and the operators above are permitted.
    """
    try:
        tree = ast.parse(expression, mode="eval")
        return _eval_node(tree.body)
    except (SyntaxError, ValueError, ZeroDivisionError, TypeError) as e:
        raise ValueError(f"Invalid expression '{expression}': {e}")
