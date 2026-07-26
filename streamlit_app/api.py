"""Small client for the FastAPI RAG service."""

import os

import requests


def get_api_url() -> str:
    return os.getenv("RAG_API_URL", "http://localhost:8000").rstrip("/")


def ask(question: str, limit: int = 5) -> dict:
    response = requests.post(
        f"{get_api_url()}/chat", json={"question": question, "limit": limit}, timeout=60
    )
    response.raise_for_status()
    return response.json()


def is_healthy() -> bool:
    try:
        return requests.get(f"{get_api_url()}/health", timeout=3).ok
    except requests.RequestException:
        return False
