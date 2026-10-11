import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER", "groq").strip().lower()

if PROVIDER == "groq":
    BASE_URL = "https://api.groq.com/openai/v1"
    API_KEY = os.getenv("GROQ_API_KEY")
    MODEL = os.getenv("MODEL", "openai/gpt-oss-120b")

else:
    raise SystemExit(
        f"Unknown PROVIDER '{PROVIDER}'. Use groq."
    )

if not API_KEY:
    raise SystemExit(
        "No API key found. Check your .env file."
    )

client = OpenAI(
    base_url=BASE_URL,
    api_key=API_KEY
)


BOOKS = {
    "Python Basics": 450,
    "Data Structures": 600,
    "Machine Learning": 750
}


def banner(system_name):
    print(
        f"\n=== {system_name} | provider: {PROVIDER} | model: {MODEL} ===\n"
    )
    