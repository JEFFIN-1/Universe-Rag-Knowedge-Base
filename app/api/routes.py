from fastapi import APIRouter
from pydantic import BaseModel
from typing import Any

from app.chat.service import ask

router = APIRouter()


class ChatRequest(BaseModel):
    question: str
    limit: int = 5


@router.post("/chat")
def chat_endpoint(request: ChatRequest):

    return ask(request.question, top_k=request.limit)
