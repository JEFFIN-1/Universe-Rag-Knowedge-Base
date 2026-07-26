"""Metadata construction for document chunks."""

from pathlib import Path

def create_metadata(chunks, pdf_path):

    filename = Path(pdf_path).name

    metadata = []

    for i, chunk in enumerate(chunks):

        metadata.append({
            "chunk_id": i,
            "document": filename,
            "source": pdf_path,
            "text": chunk
        })

    return metadata