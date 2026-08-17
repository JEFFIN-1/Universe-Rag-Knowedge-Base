import json

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

        test_case = LLMTestCase(
            input=item["question"],
            actual_output=answer,
            expected_output=item["expected_answer"],
            retrieval_context=retrieval_context,
        )

        test_cases.append(test_case)

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