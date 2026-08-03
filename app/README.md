# Application service

This package runs the RAG backend. `main.py` creates the FastAPI application, while its subpackages implement the chat flow: retrieve documents, build a grounded prompt, call the LLM, and optionally record metrics.

- `api/` defines HTTP routes.
- `chat/` orchestrates a question-to-answer request.
- `retrieval/` contains BM25, vector, and hybrid retrieval.
- `prompts/` formats retrieved context for the LLM.
- `llm/` contains the Groq client.
- `monitoring/` persists conversation measurements to PostgreSQL.
