import json
<<<<<<< HEAD

from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric,
)
from deepeval.test_case import LLMTestCase


DATASET_PATH = "evaluation/datasets/rag_eval.jsonl"


def load_dataset():
    with open(DATASET_PATH, encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def main():
    from app.chat.service import ask

    dataset = load_dataset()

    test_cases = []

    for item in dataset:
        print(f"\nRunning {item['id']}: {item['question']}")

        result = ask(item["question"])

        answer = result["answer"]

        retrieval_context = [
            source["_source"]["text"]
            for source in result["sources"]
            if "_source" in source and "text" in source["_source"]
        ]
=======
from pathlib import Path

from deepeval import evaluate
from deepeval.evaluate import AsyncConfig
from deepeval.test_case import LLMTestCase

from evaluation.rag_runner import run_rag
from evaluation.metrics import get_rag_metrics


DATASET_PATH = Path("evaluation/questions.json")


def load_questions() -> list[dict]:
    """Load the canonical evaluation dataset."""
    with DATASET_PATH.open(encoding="utf-8") as f:
        return json.load(f)


def build_test_cases(questions: list[dict]) -> list[LLMTestCase]:
    """Run the RAG and convert each result into a DeepEval test case."""

    test_cases = []

    for item in questions:
        print()
        print("=" * 80)
        print(f"{item['id']} [{item['category']}]")
        print(item["question"])
        print("=" * 80)

        result = run_rag(item["question"])

        answer = result["answer"]
        retrieval_context = result["retrieval_context"]

        print(f"Answer: {answer}")
        print(f"Retrieved chunks: {len(retrieval_context)}")
>>>>>>> 1af3b42 (update for project 2)

        test_case = LLMTestCase(
            input=item["question"],
            actual_output=answer,
            expected_output=item["expected_answer"],
            retrieval_context=retrieval_context,
        )

        test_cases.append(test_case)

<<<<<<< HEAD
    metrics = [
        FaithfulnessMetric(
            threshold=0.5,
            include_reason=True,
        ),
        AnswerRelevancyMetric(
            threshold=0.5,
            include_reason=True,
        ),
        ContextualRelevancyMetric(
            threshold=0.5,
            include_reason=True,
        ),
    ]

    evaluate(
        test_cases=test_cases,
        metrics=metrics,
    )


if __name__ == "__main__":
    main()
=======
    return test_cases


def main():
    questions = load_questions()

    print(f"Loaded {len(questions)} evaluation questions.")

    test_cases = build_test_cases(questions)

    metrics = get_rag_metrics()

    print()
    print("Running DeepEval...")
    print(f"Metrics: {len(metrics)}")

    evaluate(
    test_cases=test_cases,
    metrics=metrics,
    async_config=AsyncConfig(
        run_async=False,
        throttle_value=10,
    ),
)


if __name__ == "__main__":
    main()
>>>>>>> 1af3b42 (update for project 2)
