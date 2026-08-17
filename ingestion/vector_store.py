"""Elasticsearch storage for chunks and vector search."""

import os
from collections.abc import Sequence

from elasticsearch import Elasticsearch

INDEX_NAME = os.getenv("ELASTICSEARCH_INDEX", "pdf_documents")


def get_client() -> Elasticsearch:
    return Elasticsearch(os.getenv("ELASTICSEARCH_URL", "http://localhost:9200"))


def ensure_index(client: Elasticsearch, dimensions: int) -> None:
    if client.indices.exists(index=INDEX_NAME):
        return
    client.indices.create(
        index=INDEX_NAME,
        mappings={
            "properties": {
                "text": {"type": "text"},
                "embedding": {"type": "dense_vector", "dims": dimensions, "index": True, "similarity": "cosine"},
                "source": {"type": "keyword"},
                "filename": {"type": "keyword"},
                "page": {"type": "integer"},
                "chunk_index": {"type": "integer"},
            }
        },
    )


def index_chunks(records: Sequence[dict[str, object]]) -> int:
    if not records:
        return 0
    from elasticsearch.helpers import bulk

    client = get_client()
    ensure_index(client, len(records[0]["embedding"]))
    actions = ({"_index": INDEX_NAME, "_source": record} for record in records)
    success, _ = bulk(client, actions)
    return success
