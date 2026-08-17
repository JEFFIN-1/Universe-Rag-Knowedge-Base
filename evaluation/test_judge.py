import os

from deepeval.models import LiteLLMModel


def main():
    if not os.getenv("GROQ_API_KEY"):
        raise RuntimeError("GROQ_API_KEY is not set")

    judge = LiteLLMModel(
        model="groq/openai/gpt-oss-120b",
        api_key=os.environ["GROQ_API_KEY"],
        temperature=0,
    )

    response = judge.generate(
        "In one sentence, explain why the cosmic microwave background "
        "supports the hot Big Bang model."
    )

    print("Judge response:")
    print(response)


if __name__ == "__main__":
    main()