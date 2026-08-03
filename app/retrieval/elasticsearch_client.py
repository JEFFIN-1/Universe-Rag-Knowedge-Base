from elasticsearch import Elasticsearch

INDEX_NAME = "pdf_documents"

es = Elasticsearch(
    "http://localhost:9200"
)