"""Dependency-free, overlap-aware text chunking."""

from langchain_text_splitters import RecursiveCharacterTextSplitter

def clean_text(text):
    text = text.replace("\u200b", " ")
    text = text.replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_into_chunks(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            "? ",
            "! ",
            " ",
            ""
        ]
    )

    return splitter.split_text(text)