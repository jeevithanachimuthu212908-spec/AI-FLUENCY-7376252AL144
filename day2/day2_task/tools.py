import ast
import operator

from config import BOOKS


def get_book_price(book_name: str) -> str:

    price = BOOKS.get(book_name.strip())

    if price is not None:
        return str(price)

    return f"Unknown book: {book_name}"


_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
}


def _evaluate(node):

    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:

        return _OPS[type(node.op)](
            _evaluate(node.left),
            _evaluate(node.right)
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:

        return _OPS[type(node.op)](
            _evaluate(node.operand)
        )

    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:

    try:

        result = _evaluate(
            ast.parse(
                expression,
                mode="eval"
            ).body
        )

        return str(result)

    except Exception as error:

        return f"Calculator error: {error}"


TOOL_FUNCTIONS = {
    "get_book_price": get_book_price,
    "calculator": calculator
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_book_price",
            "description": (
                "Get the price of a book from the college library "
                "book catalog."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "book_name": {
                        "type": "string"
                    }
                },
                "required": ["book_name"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Calculate arithmetic expressions using "
                "+, -, *, / and brackets."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


if __name__ == "__main__":

    print(
        "get_book_price('Python Basics') ->",
        get_book_price("Python Basics")
    )

    print(
        "get_book_price('Data Structures') ->",
        get_book_price("Data Structures")
    )

    print(
        "calculator('(450 + 600)') ->",
        calculator("(450 + 600)")
    )
    