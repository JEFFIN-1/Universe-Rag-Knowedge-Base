# RAG Project

A small PDF retrieval-augmented generation service. PDFs enter `storage/raw/`,
are chunked and embedded into Elasticsearch, and are then available through a
FastAPI chat endpoint.

## Quick start

```bash
uv sync
docker compose up -d elasticsearch
cp .env.example .env  # or add OPENAI_API_KEY to your existing .env
python -m ingestion.register storage/raw/your-document.pdf
uv run uvicorn app.main:app --reload
```

Send a question to `POST /chat`:

```json
{"question": "What does the document say about refunds?"}
```

The API documentation is served at `http://localhost:8000/docs`.

## Layout

- `app/`: FastAPI, retrieval, prompts, and chat orchestration.
- `ingestion/`: PDF extraction through Elasticsearch registration.
- `storage/`: raw input, processed artifacts, and failed documents.
- `workflows/ingest_pdf.yaml`: documented ingestion sequence.
