"""
Text preprocessing utilities.
"""

import re


def clean_text(text: str) -> str:
    """
    Clean extracted PDF text before chunking.

    Steps:
    - Remove zero-width spaces.
    - Replace newlines with spaces.
    - Collapse multiple whitespace.
    - Trim leading/trailing whitespace.
    """

    # Remove zero-width spaces
    text = text.replace("\u200b", " ")

    # Replace newlines with spaces
    text = text.replace("\n", " ")

    # Collapse multiple whitespace
    text = re.sub(r"\s+", " ", text)

    # Trim
    return text.strip()