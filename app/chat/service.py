"""Grounded chat orchestration."""

import os

from openai import OpenAI

from app.prompts.chat import build_messages
from app.retrieval.search import search


def answer_question(question: str, limit: int = 5) -> dict[str, object]:
    documents = search(question, limit)
    completion = OpenAI(api_key=os.getenv("OPENAI_API_KEY")).chat.completions.create(
        model=os.getenv("CHAT_MODEL", "gpt-4o-mini"), messages=build_messages(question, documents), temperature=0,
    )
    return {"answer": completion.choices[0].message.content, "sources": documents}
