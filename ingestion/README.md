# Ingestion pipeline

This folder converts PDFs into searchable records. The `python -m ingestion.register <pdf>` command extracts page text, normalizes it, chunks it with overlap, generates embeddings, attaches page/source metadata, and bulk-indexes the records in Elasticsearch.

`workflows/ingest_pdf.yaml` documents the intended sequence. `elasticsearch_store.py` is a placeholder for a higher-level store implementation.
