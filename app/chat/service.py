from app.retrieval.hybrid import hybrid_search
from app.prompts.prompt_builder import build_prompt
from app.llm.client import generate_answer
import time

from app.monitoring.logger import log_conversation

def ask(question: str, top_k: int = 5) -> dict:

    start = time.perf_counter()

    documents = hybrid_search(
        query=question,
        top_k=top_k
    )

    prompt = build_prompt(
        query=question,
        documents=documents
    )

    answer = generate_answer(prompt)

    response_time = time.perf_counter() - start

    # Monitoring must not make a successful chat request fail when PostgreSQL is
    # not configured or unavailable.
    try:
        log_conversation(
            question=question,
            answer=answer,
            response_time=response_time,
            retrieved_chunks=len(documents),
            model="llama"
        )
    except Exception as exc:
        print(f"Monitoring skipped: {exc}")

    return {
        "answer": answer,
        "sources": documents
    }
