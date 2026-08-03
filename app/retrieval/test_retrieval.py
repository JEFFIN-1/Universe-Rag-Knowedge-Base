from app.retrieval.vector import vector_search
from app.retrieval.bm25 import bm25_search
from app.retrieval.hybrid import hybrid_search

query = "What is reinforcement learning?"

print("\nVECTOR SEARCH")
print("=" * 60)

for hit in vector_search(query):
    print(hit["_score"])
    print(hit["_source"]["text"][:150])
    print()

print("\nBM25 SEARCH")
print("=" * 60)

for hit in bm25_search(query):
    print(hit["_score"])
    print(hit["_source"]["text"][:150])
    print()

print("\nHYBRID SEARCH (RRF)")
print("=" * 60)

for hit in hybrid_search(query):
    print(hit["_source"]["text"][:150])
    print()