SYSTEM_PROMPT = """
You are a helpful AI assistant.

Use ONLY the provided context to answer the user's question.

If the answer cannot be found in the context, say:

"I don't have enough information in the provided documents."

Do not invent facts.
"""


def build_prompt(query: str, documents: list) -> str:
    context = []

    for i, hit in enumerate(documents, start=1):
        source = hit["_source"]

        context.append(
            f"""### Document {i}
Source: {source["source"]}

{source["text"]}
"""
        )

    context_text = "\n\n".join(context)

    prompt = f"""{SYSTEM_PROMPT}

Context:
{context_text}

Question:
{query}

Answer:
"""

    return prompt