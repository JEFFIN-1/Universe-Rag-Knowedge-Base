from .vector import vector_search
from .bm25 import bm25_search


def reciprocal_rank_fusion(results_list, k=60):
    """
    Combine multiple ranked result lists using Reciprocal Rank Fusion (RRF).
    """
    fused_scores = {}

    for results in results_list:
        for rank, hit in enumerate(results):
            doc_id = hit["_id"]

            if doc_id not in fused_scores:
                fused_scores[doc_id] = {
                    "score": 0,
                    "hit": hit
                }

            fused_scores[doc_id]["score"] += 1 / (k + rank + 1)

    reranked = sorted(
        fused_scores.values(),
        key=lambda x: x["score"],
        reverse=True
    )

    return [item["hit"] for item in reranked]


def hybrid_search(query, top_k=5):

    candidate_k = 10

    vector_results = vector_search(query, candidate_k)
    bm25_results = bm25_search(query, candidate_k)

    fused = reciprocal_rank_fusion(
        [vector_results, bm25_results]
    )

    return fused[:top_k]
