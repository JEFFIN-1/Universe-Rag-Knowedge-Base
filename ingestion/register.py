"""Command-line entry point that registers a PDF in the vector store."""

import argparse
from pathlib import Path

from ingestion.chunk import chunk_text
from ingestion.embeddings import embed_texts
from ingestion.extract_pdf import extract_pdf
from ingestion.metadata import document_metadata
from ingestion.normalize import normalize_text
from ingestion.vector_store import index_chunks


def ingest_pdf(path: str | Path, chunk_size: int = 800, overlap: int = 120) -> int:
    records: list[dict[str, object]] = []
    for page in extract_pdf(path):
        chunks = chunk_text(normalize_text(str(page["text"])), chunk_size, overlap)
        vectors = embed_texts(chunks) if chunks else []
        for index, (text, vector) in enumerate(zip(chunks, vectors)):
            records.append({"text": text, "embedding": vector, **document_metadata(path, int(page["page"]), index)})
    return index_chunks(records)


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest a PDF into Elasticsearch.")
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()
    print(f"Indexed {ingest_pdf(args.pdf)} chunks.")


if __name__ == "__main__":
    main()
