"""HTTP routes for the RAG service."""

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.chat.service import answer_question

router = APIRouter()


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=4_000)
    limit: int = Field(default=5, ge=1, le=20)


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/chat")
def chat(request: ChatRequest) -> dict[str, object]:
    return answer_question(request.question, request.limit)
