"""Dependency-free, overlap-aware text chunking."""

from langchain_text_splitters import RecursiveCharacterTextSplitter

def split_into_chunks(text):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=200,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    return splitter.split_text(text)