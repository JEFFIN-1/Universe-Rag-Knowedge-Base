import json
import os

from deepeval import evaluate
from deepeval.models import LiteLLMModel
from deepeval.metrics import (
    FaithfulnessMetric,
)
from deepeval.test_case import LLMTestCase


DATASET_PATH = "evaluation/datasets/rag_eval.jsonl"


def load_first_question():
    with open(DATASET_PATH, encoding="utf-8") as f:
        return json.loads(next(f))


def main():
    from app.chat.service import ask

    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not set")

    item = load_first_question()

    print(f"\nEvaluating {item['id']}")
    print(f"Question: {item['question']}")

    result = ask(item["question"])

    actual_output = result["answer"]

    retrieval_context = [
        source["_source"]["text"]
        for source in result["sources"]
        if "_source" in source and "text" in source["_source"]
    ]

    print(f"Retrieved contexts: {len(retrieval_context)}")

    judge_model = LiteLLMModel(
        model="groq/openai/gpt-oss-120b",
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0,
    )

    test_case = LLMTestCase(
        input=item["question"],
        actual_output=actual_output,
        expected_output=item["expected_answer"],
        retrieval_context=retrieval_context,
    )

    metrics = [
    FaithfulnessMetric(
        threshold=0.5,
        model=judge_model,
        include_reason=False,
    ),

]

    print("\nRunning DeepEval...\n")

    results = evaluate(
        test_cases=[test_case],
        metrics=metrics,
    )

    print("\nEvaluation finished.")
    print(results)


if __name__ == "__main__":
    main()