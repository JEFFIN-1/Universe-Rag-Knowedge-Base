import os

from dotenv import load_dotenv
from deepeval.models import OpenRouterModel
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
)

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    raise RuntimeError(
        "OPENROUTER_API_KEY is not configured. "
        "Make sure it is available in your .env file."
    )


def get_judge_model():
    return OpenRouterModel(
        model="openrouter/free",
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
    )


def get_rag_metrics():
    judge = get_judge_model()

    return [
        FaithfulnessMetric(
            threshold=0.5,
            include_reason=False,
            model=judge,
        ),
        AnswerRelevancyMetric(
            threshold=0.5,
            include_reason=False,
            model=judge,
        ),
    ]