"""Text cleanup shared by ingestion stages."""

import re


def normalize_text(text: str) -> str:
    """Collapse whitespace while retaining paragraph boundaries."""
    paragraphs = (re.sub(r"\s+", " ", part).strip() for part in text.split("\n\n"))
    return "\n\n".join(paragraph for paragraph in paragraphs if paragraph)
