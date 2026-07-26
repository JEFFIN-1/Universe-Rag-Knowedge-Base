import re

def clean_text(text):
    """
    Basic text cleaning
    """

    text = text.replace("\n", " ")

    text = re.sub(r"\s+", " ", text)

    text = text.strip()

    return text