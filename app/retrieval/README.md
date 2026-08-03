# Retrieval

This package contains the search layer:

- `bm25.py` performs Elasticsearch keyword retrieval.
- `vector.py` performs dense-vector nearest-neighbor retrieval.
- `hybrid.py` merges ranked results with Reciprocal Rank Fusion (RRF).
- `search.py` provides an alternate semantic-search helper used with the ingestion vector-store configuration.

The modules currently use different index/model configurations and should be consolidated before production deployment.
