from sentence_transformers import SentenceTransformer
from .elasticsearch_client import es, INDEX_NAME

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def vector_search(query, top_k=5):

    query_vector = model.encode(query).tolist()

    response = es.search(
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