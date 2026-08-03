# ingestion/embeddings.py

import numpy as np

from embedder.embedder import Embedder


model = Embedder()


def embed_documents(texts):

    embeddings = model.encode_batch(texts)

    return np.asarray(
        embeddings,
        dtype=np.float32,
    ).tolist()


def embed_query(text):

    embedding = model.encode(text)

    return np.asarray(
        embedding,
        dtype=np.float32,
    ).tolist()

