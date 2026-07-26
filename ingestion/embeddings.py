# ingestion/embeddings.py

from sentence_transformers import SentenceTransformer

# Load the model only once
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def embed_documents(texts):
    """
    Generate embeddings for multiple texts.
    """
    return model.encode(
        texts,
        batch_size=32,
        convert_to_numpy=True
    ).tolist()


def embed_query(text):
    """
    Generate embedding for a single query.
    """
    return model.encode(
        [text],
        convert_to_numpy=True
    )[0].tolist()