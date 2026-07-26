"""Semantic retrieval used by the chat service."""

from ingestion.embeddings import embed_texts
from ingestion.vector_store import INDEX_NAME, get_client


def search(query: str, limit: int = 5) -> list[dict[str, object]]:
    vector = embed_texts([query])[0]
    response = get_client().search(
        index=INDEX_NAME,
        knn={"field": "embedding", "query_vector": vector, "k": limit, "num_candidates": max(limit * 10, 50)},
        source=["text", "source", "filename", "page", "chunk_index"],
    )
    return [{**hit["_source"], "score": hit["_score"]} for hit in response["hits"]["hits"]]
