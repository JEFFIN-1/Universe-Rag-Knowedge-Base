"""PDF text extraction for the ingestion pipeline."""

from pathlib import Path


def extract_pdf(path: str | Path) -> list[dict[str, object]]:
    """Return one text record per page in *path*.

    ``pypdf`` is imported here so the API can be used without PDF support
    installed until ingestion is actually run.
    """
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - installation error
        raise RuntimeError("Install pypdf to ingest PDF files.") from exc

    file_path = Path(path)
    reader = PdfReader(str(file_path))
    return [
        {"page": number, "text": page.extract_text() or ""}
        for number, page in enumerate(reader.pages, start=1)
    ]
