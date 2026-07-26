SYSTEM_PROMPT = """You answer only from the supplied context. If the context does not
contain the answer, say that you do not know. Cite sources using [filename, p. N]."""


def build_messages(question: str, documents: list[dict[str, object]]) -> list[dict[str, str]]:
    context = "\n\n".join(
        f"[{doc['filename']}, p. {doc['page']}]\n{doc['text']}" for doc in documents
    )
    return [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]
