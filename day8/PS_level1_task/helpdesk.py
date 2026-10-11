import ast
import operator
import os

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from settings import VECTOR_DIR, HashEmbeddings, MAX_DISTANCE

load_dotenv()

SYSTEM_PROMPT = """
You are the Greenfield College helpdesk agent.

Rules:
1. Use search_handbook for college policies and handbook questions.
2. Use check_exam_eligibility for exam attendance questions.
3. Use get_course_fee for course fee questions.
4. Use calculator for arithmetic. Do not calculate mentally.
5. If search_handbook returns NO_MATCH, say:
   "I don't know; this is not covered in the college handbook."
6. Never invent college policies or fee values.
7. For follow-up questions, use relevant conversation history.
8. Answer concisely and accurately.
"""


def get_store():
    return Chroma(
        collection_name="college_handbook",
        persist_directory=str(VECTOR_DIR),
        embedding_function=HashEmbeddings(),
        collection_metadata={"hnsw:space": "cosine"}
    )


@tool
def search_handbook(query: str) -> str:
    """Search college handbook chunks using a relevance threshold."""
    store = get_store()

    results = store.similarity_search_with_score(
        query, k=3
    )

    relevant = [
        (doc, float(score))
        for doc, score in results
        if float(score) <= MAX_DISTANCE
    ]

    if not relevant:
        return "NO_MATCH: this is not covered in the college handbook."

    output = []

    for doc, score in relevant:
        source = doc.metadata.get("source", "unknown")
        output.append(
            f"[source={source}; distance={score:.4f}]\n"
            f"{doc.page_content}"
        )

    return "\n\n".join(output)


@tool
def check_exam_eligibility(attendance_percent: float) -> str:
    """Check exam eligibility for attendance between 0 and 100."""
    if not 0 <= attendance_percent <= 100:
        return "ERROR: attendance must be between 0 and 100."

    if attendance_percent >= 75:
        return (
            "ELIGIBLE: attendance is 75% or above; "
            "the student may write the end-semester exam."
        )

    if attendance_percent >= 65:
        return (
            "CONDONATION: attendance is 65% to below 75%; "
            "condonation is required at Rs. 500 per course."
        )

    return (
        "NOT ELIGIBLE: attendance is below 65%; "
        "the student may not write the end-semester exam."
    )


@tool
def get_course_fee(course_code: str) -> str:
    """Get the fee for a course such as CS101 or AI202."""
    fees = {
        "CS101": 12000,
        "AI202": 18000
    }

    code = course_code.strip().upper()

    if code not in fees:
        return f"ERROR: no fee record for {code}."

    return f"{code} course fee: Rs. {fees[code]}"


ALLOWED_BINARY = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod
}

ALLOWED_UNARY = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg
}


def safe_calculate(expression):
    """Evaluate arithmetic only; never execute arbitrary Python code."""
    tree = ast.parse(expression, mode="eval")

    def visit(node):
        if isinstance(node, ast.Expression):
            return visit(node.body)

        if (
            isinstance(node, ast.Constant)
            and type(node.value) in (int, float)
        ):
            return node.value

        if (
            isinstance(node, ast.BinOp)
            and type(node.op) in ALLOWED_BINARY
        ):
            left = visit(node.left)
            right = visit(node.right)
            return ALLOWED_BINARY[type(node.op)](left, right)

        if (
            isinstance(node, ast.UnaryOp)
            and type(node.op) in ALLOWED_UNARY
        ):
            return ALLOWED_UNARY[type(node.op)](visit(node.operand))

        raise ValueError("Only basic arithmetic is allowed.")

    return visit(tree)


@tool
def calculator(expression: str) -> str:
    """Calculate arithmetic using +, -, *, /, // or %."""
    try:
        result = safe_calculate(expression)
        return f"Result: {result}"
    except (SyntaxError, ValueError, ZeroDivisionError) as exc:
        return f"ERROR: invalid arithmetic expression: {exc}"


tools = [
    search_handbook,
    check_exam_eligibility,
    get_course_fee,
    calculator
]


def main():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise SystemExit("Set OPENAI_API_KEY in your .env file.")

    model = ChatOpenAI(
        model=os.getenv("CHAT_MODEL", "openai/gpt-oss-20b"),
        api_key=api_key,
        base_url=os.getenv(
            "OPENAI_BASE_URL",
            "https://api.groq.com/openai/v1"
        ),
        temperature=0
    )

    agent = create_react_agent(
        model,
        tools,
        prompt=SYSTEM_PROMPT,
        checkpointer=MemorySaver()
    )

    config = {
        "configurable": {
            "thread_id": "task-run"
        }
    }

    print("=== DIRECT EXAM TOOL TESTS ===")

    for value in (82, 70, 50, 120):
        answer = check_exam_eligibility.invoke({
            "attendance_percent": value
        })
        print(f"{value}: {answer}")

    questions = [
        "What CGPA do I need to be eligible for placements?",
        "My attendance is 70%. Can I write the exam?",
        "What is the total of the CS101 fee, the AI202 fee and the maximum late fee?",
        "And if I pay only 5 days late instead?",
        "What is the capital of France?"
    ]

    previous_count = 0

    for number, question in enumerate(questions, start=1):
        print(f"\n{'=' * 12} QUESTION {number} {'=' * 12}")
        print("USER:", question)

        try:
            result = agent.invoke(
                {
                    "messages": [
                        {"role": "user", "content": question}
                    ]
                },
                config=config
            )

            messages = result.get("messages", [])
            new_messages = messages[previous_count:]
            previous_count = len(messages)

            for message in new_messages:
                if getattr(message, "type", "") == "tool":
                    print(
                        f"TOOL [{message.name}]: "
                        f"{message.content}"
                    )

            if messages:
                print("ASSISTANT:", messages[-1].content)

        except Exception as exc:
            print("AGENT ERROR:", repr(exc))


if __name__ == "__main__":
    main()
    