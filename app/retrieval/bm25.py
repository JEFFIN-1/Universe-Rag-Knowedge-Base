from ingestion.vector_store import INDEX_NAME, get_client


def bm25_search(query, top_k=5):

    response = get_client().search(
        index=INDEX_NAME,
        query={
            "match": {
                "text": query
            }
        },
        size=top_k,
        source=["text", "page", "source"],
    )

    return response["hits"]["hits"]
