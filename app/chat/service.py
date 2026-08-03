from app.retrieval.hybrid import hybrid_search
from app.prompts.prompt_builder import build_prompt
from app.llm.client import generate_answer


def ask(question: str, top_k: int = 5) -> dict:
    """
    Complete RAG pipeline.

    Returns:
        {
            "answer": "...",
            "documents": [...]
        }
    """

    documents = hybrid_search(
        query=question,
        top_k=top_k
    )

    prompt = build_prompt(
        query=question,
        documents=documents
    )

    answer = generate_answer(prompt)

    return {
        "answer": answer,
        "documents": documents
    }