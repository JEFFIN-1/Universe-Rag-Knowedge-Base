from app.chat.service import ask


def run_rag(question: str, top_k: int = 5) -> dict:
    """
    Run the production RAG pipeline for evaluation.

    Returns:
        {
            "answer": str,
            "sources": list,
            "retrieval_context": list[str]
        }
    """
    result = ask(question, top_k=top_k)

    retrieval_context = [
        source["_source"]["text"]
        for source in result["sources"]
        if "_source" in source and "text" in source["_source"]
    ]

    return {
        "answer": result["answer"],
        "sources": result["sources"],
        "retrieval_context": retrieval_context,
    }