from .elasticsearch_client import es, INDEX_NAME


def bm25_search(query, top_k=5):

    response = es.search(
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