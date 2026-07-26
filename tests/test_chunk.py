from ingestion.chunk import chunk_text
from ingestion.normalize import normalize_text


def test_normalize_text_collapses_inline_whitespace() -> None:
    assert normalize_text(" one\t two  \nthree ") == "one two three"


def test_chunk_text_preserves_overlap() -> None:
    chunks = chunk_text("one two three four five six", chunk_size=13, overlap=4)
    assert len(chunks) > 1
    assert chunks[0]
    assert chunks[1]
