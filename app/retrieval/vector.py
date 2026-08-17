"""Dense-vector retrieval using the checked-in local ONNX embedding model."""

from ingestion.embeddings import embed_query
from ingestion.vector_store import INDEX_NAME, get_client


def vector_search(query, top_k=5):
    query_vector = embed_query(query)

    response = get_client().search(
        index=INDEX_NAME,
        knn={
            "field": "embedding",
            "query_vector": query_vector,
            "k": top_k,
            "num_candidates": 100,
        },
        source=["text", "page", "source"],
    )

    return response["hits"]["hits"]
