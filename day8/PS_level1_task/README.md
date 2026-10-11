# College Helpdesk Agent — Day 8

A college helpdesk agent built with Python, LangChain, LangGraph
and ChromaDB using offline hash embeddings.

## Features

- College handbook retrieval
- Placement eligibility lookup
- Exam attendance eligibility tool
- Course fee lookup
- Arithmetic calculator
- Relevance guard using cosine distance
- Conversation memory using a thread ID

## Setup

Create and activate a Python virtual environment:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the packages:

```powershell
pip install langchain-core langchain-openai langchain-chroma langchain-text-splitters langgraph python-dotenv chromadb
```

Copy `.env.example` to `.env`, or create `.env` manually.
Configure the chat API key and keep `EMBED_PROVIDER=hash`.

## Run

```powershell
python build_index.py
python search_test.py
python helpdesk.py
```

Save terminal output:

```powershell
python helpdesk.py > execution_log.txt 2>&1
```

## Limitations

Hash embeddings are deterministic and local but do not have the
semantic understanding of trained embedding models.

The chat model requires API access. Its tool selection and final
answers must be evaluated from actual test runs.

Do not commit `.env` or the generated vector store.
