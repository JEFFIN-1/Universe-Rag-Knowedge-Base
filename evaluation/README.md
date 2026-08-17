# RAG Evaluation with DeepEval

This directory contains the evaluation layer for the RAG application in
this project.

The evaluation goal is **not** simply to determine whether the LLM
produces a plausible answer. The goal is to measure the complete RAG
pipeline and identify whether a failure comes from:

1.  retrieval,
2.  prompt/context construction,
3.  generation,
4.  grounding/faithfulness, or
5.  the quality of the reference answer.

The project uses **DeepEval** as the primary evaluation framework and
**LLM-as-a-Judge** for semantic evaluation.

------------------------------------------------------------------------

## 1. Why this evaluation layer exists

The application currently follows this pipeline:

``` text
User Question
     |
     v
Embedding
     |
     v
Elasticsearch
     |
     +--> Vector Search
     |
     +--> BM25 Search
     |
     v
Hybrid Search / RRF
     |
     v
Top-K Retrieved Chunks
     |
     v
Prompt Builder
     |
     v
Groq LLM
     |
     v
Generated Answer
```

The evaluation pipeline wraps this existing application without creating
a second RAG implementation:

``` text
Evaluation Question
        |
        v
app.chat.service.ask()
        |
        +--------------------+
        |                    |
        v                    v
   Actual Answer       Retrieved Chunks
        |                    |
        +---------+----------+
                  |
                  v
            DeepEval
                  |
        +---------+---------+
        |                   |
        v                   v
  Generator Metrics   Retriever Metrics
        |                   |
        +---------+---------+
                  |
                  v
             Evaluation
               Report
```

**Important:** the evaluation code should call the existing `ask()`
function. It should not duplicate retrieval, prompt building, or LLM
generation logic.

------------------------------------------------------------------------

# 2. Current project state

The RAG application has already implemented:

-   PDF ingestion
-   PDF extraction
-   preprocessing
-   chunking
-   metadata
-   embeddings
-   Elasticsearch indexing
-   vector search
-   BM25 search
-   hybrid search using Reciprocal Rank Fusion (RRF)
-   prompt construction
-   Groq LLM generation
-   conversation logging

The current RAG entry point is:

``` python
from app.chat.service import ask

result = ask("your question")
```

The returned object contains:

``` python
{
    "answer": "...",
    "sources": [...]
}
```

Therefore the evaluation layer can directly obtain:

-   `actual_output` from `result["answer"]`
-   `retrieval_context` from `result["sources"]`

------------------------------------------------------------------------

# 3. Why DeepEval instead of evaluating manually?

Manual evaluation is useful for debugging a few examples, but it does
not scale.

For example, a human can inspect:

``` text
Question
Retrieved chunks
Generated answer
Reference answer
```

and decide whether the answer is good.

However, once there are 10, 50, or 500 questions, we need consistent
measurements.

DeepEval provides LLM-as-a-Judge metrics for RAG systems. Its current
RAG evaluation surface separates retriever and generator quality.

The main native RAG metrics are:

### Retriever

-   `ContextualRelevancyMetric`
-   `ContextualPrecisionMetric`
-   `ContextualRecallMetric`

### Generator

-   `AnswerRelevancyMetric`
-   `FaithfulnessMetric`

DeepEval's documentation recommends treating retrieval and generation as
separate components because a poor final answer can be caused by either
bad retrieval or bad generation.

Official documentation:

-   DeepEval RAG Evaluation
-   DeepEval RAG Evaluation Quickstart
-   DeepEval Faithfulness
-   DeepEval Answer Relevancy
-   DeepEval Contextual Relevancy
-   DeepEval Contextual Precision
-   DeepEval Contextual Recall

See the official DeepEval documentation for the current API because
metric APIs and supported judge providers can evolve.

------------------------------------------------------------------------

# 4. Evaluation philosophy for this project

The evaluation dataset must be designed around the **knowledge actually
contained in the ingested PDFs**.

This is critical.

For example:

``` text
Question:
What is the universe?
```

may be a perfectly reasonable general-knowledge question, but it is a
poor RAG benchmark if the retrieved documents only discuss:

-   the origin of the universe,
-   Big Bang cosmology,
-   multiverse hypotheses,
-   FLRW cosmology,
-   philosophical questions about cosmic origins.

If the retrieved context does not directly define the universe, the
correct RAG behavior may be:

``` text
I don't have enough information in the provided documents.
```

That is not necessarily a failed RAG response. It can demonstrate
correct grounding and refusal behavior.

Therefore:

> Evaluation questions should be answerable from the project knowledge
> base when they are intended to test successful retrieval and
> generation.

A smaller number of deliberately unanswerable questions can be included
to test hallucination/refusal behavior.

------------------------------------------------------------------------

# 5. Question categories

The first evaluation dataset should contain approximately 10 questions.

Recommended distribution:

``` text
3 factual
3 conceptual
2 numerical / application
2 unanswerable or out-of-context
```

## 5.1 Factual questions

These test whether the system can retrieve explicitly stated
information.

Example:

``` text
What is the standard cosmological model based on?
```

A good answer should be directly supported by the retrieved documents.

Factual questions mainly test:

-   retrieval
-   extraction
-   grounding
-   answer correctness

------------------------------------------------------------------------

## 5.2 Conceptual questions

These require synthesis or explanation rather than copying a sentence.

Example:

``` text
Why is asking what happened before the Big Bang problematic in standard cosmology?
```

A good answer must combine relevant information from the context while
remaining faithful to it.

Conceptual questions test:

-   retrieval quality
-   context sufficiency
-   synthesis
-   faithfulness
-   answer relevance

------------------------------------------------------------------------

## 5.3 Numerical / application questions

These test whether the RAG system can retrieve relevant values,
equations, assumptions, or definitions and then apply them.

For example, if a document supplies a numerical relationship or physical
parameter, the question can ask the model to calculate or derive
something from those supplied values.

The expected answer should make clear which document-provided
information is being used.

Numerical questions are especially useful because a model can sound
convincing while producing an incorrect calculation.

For numerical evaluation, correctness should be checked against a
human-verified reference answer rather than relying only on semantic
similarity.

------------------------------------------------------------------------

## 5.4 Unanswerable questions

These deliberately ask for information absent from the knowledge base.

Example pattern:

``` text
According to the documents, what is [topic that is clearly absent]?
```

The desired behavior is not to use the model's pretrained knowledge.

The desired behavior is a grounded refusal such as:

``` text
I don't have enough information in the provided documents.
```

These cases are useful for measuring hallucination resistance.

------------------------------------------------------------------------

# 6. Reference answers / expected answers

There are two different concepts that must not be confused.

## Ground truth

A human-verified expected answer describing what the documents support.

Example:

``` json
{
  "question": "What is the standard cosmological model based on?",
  "expected_answer": "The document states that the standard cosmological model is based on the Friedmann–Lemaître–Robertson–Walker (FLRW) solution of Einstein's equations."
}
```

## Actual answer

The answer produced by the real RAG application:

``` python
result["answer"]
```

DeepEval compares the actual output against the appropriate evaluation
criteria.

Reference answers are particularly important for reference-based metrics
such as contextual precision and contextual recall.

However, not every useful RAG metric requires a reference answer. For
example:

-   Faithfulness evaluates the actual answer against retrieved context.
-   Answer relevancy evaluates the answer against the input.
-   Contextual relevancy evaluates retrieved context against the input.

Therefore, this project should maintain references even when a
particular metric does not require them.

------------------------------------------------------------------------

# 7. Test case structure

A conceptual evaluation record should contain:

``` json
{
  "id": "q01",
  "category": "factual",
  "question": "What is the standard cosmological model based on?",
  "expected_answer": "The standard cosmological model is based on the Friedmann–Lemaître–Robertson–Walker solution of Einstein's equations.",
  "source": "In modern scientific terms.pdf"
}
```

The runtime evaluation converts this into a DeepEval `LLMTestCase`.

Conceptually:

``` python
LLMTestCase(
    input=question,
    actual_output=answer,
    expected_output=expected_answer,
    retrieval_context=retrieved_context,
)
```

The exact DeepEval constructor and parameter names should be checked
against the installed version if the API changes.

------------------------------------------------------------------------

# 8. Recommended evaluation metrics

For the first baseline, use a small, focused metric set rather than
dozens of metrics.

DeepEval currently recommends keeping evaluation runs relatively
focused.

## 8.1 Faithfulness

``` text
FaithfulnessMetric
```

Question being evaluated:

> Does the generated answer remain factually supported by the retrieved
> context?

This is one of the most important metrics for this project.

For example, if the retrieved context says:

``` text
The standard cosmological model is based on FLRW.
```

but the generated answer adds unsupported claims about unrelated
theories, faithfulness should decrease.

DeepEval describes faithfulness as evaluating whether the actual output
factually aligns with the retrieval context.

------------------------------------------------------------------------

## 8.2 Answer Relevancy

``` text
AnswerRelevancyMetric
```

Question:

> Does the generated answer actually answer the user's question?

A response can be faithful but still fail to answer the question
directly.

For example:

``` text
Question:
What is FLRW?

Answer:
The universe has an origin and cosmology is complicated...
```

This may contain true statements but still be poorly relevant.

------------------------------------------------------------------------

## 8.3 Contextual Relevancy

``` text
ContextualRelevancyMetric
```

Question:

> Are the retrieved chunks relevant to the user's question?

This directly evaluates the retrieval output.

For example, if five chunks are retrieved and four are about unrelated
topics, contextual relevancy should suffer.

------------------------------------------------------------------------

## 8.4 Contextual Precision

``` text
ContextualPrecisionMetric
```

Question:

> Are the relevant retrieved chunks ranked above irrelevant chunks?

This is particularly relevant to the hybrid-search/RRF implementation.

It evaluates retrieval ordering rather than merely asking whether
relevant information appears somewhere.

Because this is reference-based, the test case should contain a suitable
expected output.

------------------------------------------------------------------------

## 8.5 Contextual Recall

``` text
ContextualRecallMetric
```

Question:

> Did the retrieved context contain enough of the information needed to
> answer the question?

This helps identify cases where the system retrieved only part of the
necessary evidence.

For example:

``` text
Question requires:
A + B + C

Retrieved:
A + B
```

The context may be relevant but incomplete.

------------------------------------------------------------------------

# 9. RAG Triad

A useful initial three-metric view is the RAG triad:

``` text
             Question
             /      \
            /        \
           v          v
   Context Relevancy  Answer Relevancy
           \          /
            \        /
             v      v
           Faithfulness
```

These answer three important questions:

1.  Did we retrieve useful context?
2.  Did we answer the question?
3.  Did we remain grounded in the retrieved context?

The RAG triad is useful for quick diagnosis.

For a more comprehensive baseline, add:

``` text
Contextual Precision
Contextual Recall
```

This gives the full five-metric RAG evaluation set.

------------------------------------------------------------------------

# 10. How to interpret failures

Do not treat every low score as the same problem.

## Case A: Low contextual relevancy

``` text
Contextual Relevancy ↓
Faithfulness    ?
Answer Relevancy ?
```

Likely problem:

``` text
Retriever
```

Investigate:

-   embedding model
-   query formulation
-   chunk size
-   chunk overlap
-   top_k
-   BM25 configuration
-   vector search
-   RRF weighting/ranking

------------------------------------------------------------------------

## Case B: Good retrieval but low faithfulness

``` text
Contextual Relevancy ↑
Contextual Recall   ↑
Faithfulness        ↓
```

Likely problem:

``` text
Generator / prompt / model
```

Investigate:

-   prompt instructions
-   model behavior
-   temperature
-   unsupported claims
-   context formatting

------------------------------------------------------------------------

## Case C: Good faithfulness but low answer relevancy

``` text
Faithfulness      ↑
Answer Relevancy  ↓
```

The model may be faithfully discussing the context but failing to
directly answer the user's question.

Investigate:

-   prompt design
-   answer structure
-   verbosity
-   question interpretation

------------------------------------------------------------------------

## Case D: Good relevancy but low recall

``` text
Contextual Relevancy ↑
Contextual Recall   ↓
```

The retrieved chunks are relevant but incomplete.

Investigate:

-   top_k
-   chunking
-   document coverage
-   vector retrieval
-   BM25 retrieval
-   hybrid fusion

------------------------------------------------------------------------

## Case E: High scores but bad human judgment

This is a warning sign.

LLM-as-a-Judge is itself a model-based evaluation method. It is not an
absolute ground truth.

When this occurs:

1.  inspect the test case,
2.  inspect the retrieved chunks,
3.  inspect the judge's reason,
4.  compare against the reference answer,
5.  revise the evaluation criteria if necessary.

Do not blindly optimize the RAG system for a single judge score.

------------------------------------------------------------------------

# 11. LLM-as-a-Judge

DeepEval's standard RAG metrics are primarily LLM-as-a-Judge
evaluations.

The judge receives information such as:

``` text
Question
Retrieved Context
Actual Answer
Expected Answer (when required)
```

and produces a score and reason.

Conceptually:

``` text
                  Evaluation LLM
                       |
        +--------------+--------------+
        |              |              |
     Question       Context        Answer
        |              |              |
        +--------------+--------------+
                       |
                       v
                 Score + Reason
```

The judge is **not the same thing as the RAG model**.

This distinction is important.

``` text
RAG generation model:
Groq -> openai/gpt-oss-120b
```

Evaluation model:

``` text
Separate LLM-as-Judge
```

Keeping the judge logically separate reduces the chance that we
accidentally evaluate the system using the same generation output
without an independent evaluation process.

DeepEval supports custom evaluation LLMs by wrapping them with
`DeepEvalBaseLLM`, so the project does not have to be tied to OpenAI.
The current DeepEval documentation explicitly supports custom LLMs and
multiple providers.

------------------------------------------------------------------------

# 12. Judge-model policy for this project

The application model and evaluation model should be treated separately.

Current application model:

``` text
openai/gpt-oss-120b
via Groq
```

The evaluation judge can be:

-   a supported DeepEval provider,
-   an OpenAI-compatible provider,
-   a local/Ollama model,
-   or a custom `DeepEvalBaseLLM` wrapper.

Do **not** automatically assume that `GROQ_API_KEY` will configure
DeepEval. DeepEval's default provider and provider-specific
configuration are separate from the application's Groq client.

If we want to use Groq as the judge, implement it deliberately as a
DeepEval custom model and verify structured/JSON output compatibility.

For the first evaluation milestone, prioritize **reliable judge output**
over minimizing every possible API cost.

------------------------------------------------------------------------

# 13. Installation

From the project root:

``` bash
uv add deepeval
```

Verify:

``` bash
uv run python -c "import deepeval; print(deepeval.__version__)"
```

Also verify:

``` bash
uv run deepeval --help
```

DeepEval's current quickstart documents installation with:

``` bash
pip install -U deepeval[inspect]
```

The `[inspect]` extra is optional and is more appropriate for
development environments. With this project using `uv`, prefer adding
the dependency through `uv`.

------------------------------------------------------------------------

# 14. Environment variables

The existing application uses:

``` text
GROQ_API_KEY
```

Do not put secrets directly into Python files.

Keep secrets in:

``` text
.env
```

and ensure `.env` is ignored by Git.

Example:

``` text
GROQ_API_KEY=...
```

The evaluation judge may require a separate provider key depending on
which judge is selected.

Never commit:

``` text
.env
```

or API keys into the repository.

------------------------------------------------------------------------

# 15. Suggested evaluation directory

The target structure is:

``` text
eval/
├── README.md
├── questions.json
├── run_eval.py
├── results.json
└── test_eval.py
```

Optional later:

``` text
eval/
├── judges/
│   └── groq_judge.py
├── datasets/
│   ├── questions.json
│   └── questions_v2.json
└── results/
    ├── baseline.json
    └── after_retrieval_fix.json
```

Recommended responsibilities:

### `questions.json`

Human-reviewed evaluation dataset.

### `run_eval.py`

Runs the real RAG application and DeepEval metrics.

### `results.json`

Stores a machine-readable snapshot of results.

### `test_eval.py`

Optional regression tests for CI/CD.

### `judges/`

Contains custom DeepEval LLM wrappers if needed.

------------------------------------------------------------------------

# 16. Recommended first dataset

Start small.

Use 10 questions:

``` text
Q01 factual
Q02 factual
Q03 factual

Q04 conceptual
Q05 conceptual
Q06 conceptual

Q07 numerical/application
Q08 numerical/application

Q09 unanswerable
Q10 unanswerable
```

Every answerable question must be checked manually against the PDFs
before it is included.

The purpose of the first dataset is not statistical perfection.

The purpose is to establish a **baseline**.

Later, increase the dataset to:

``` text
25
50
100+
```

as the project becomes more mature.

------------------------------------------------------------------------

# 17. Do not use random questions

Bad evaluation design:

``` text
What is the capital of France?
Who invented the telephone?
What is quantum entanglement?
```

unless the PDFs actually contain those topics.

These questions mostly measure the model's general knowledge rather than
the quality of your RAG system.

Better:

``` text
What does the document say about the FLRW solution?
Why is the period before the Big Bang difficult to define?
What does the document say about multiverse hypotheses?
```

These questions test the actual knowledge base.

------------------------------------------------------------------------

# 18. Answerable versus unanswerable cases

The dataset should explicitly distinguish:

``` json
{
  "id": "q09",
  "category": "unanswerable",
  "answerable": false
}
```

This prevents a common evaluation mistake.

A refusal is not automatically a bad answer.

For an unanswerable question:

``` text
"I don't have enough information in the provided documents."
```

may be the correct behavior.

For an answerable question:

``` text
"I don't have enough information..."
```

is a failure.

Therefore the evaluation dataset needs to tell us which behavior is
expected.

------------------------------------------------------------------------

# 19. Evaluation execution

The conceptual implementation is:

``` python
from deepeval import evaluate
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    ContextualRelevancyMetric,
    ContextualPrecisionMetric,
    ContextualRecallMetric,
)
from deepeval.test_case import LLMTestCase

from app.chat.service import ask
```

For every question:

``` python
result = ask(question)

test_case = LLMTestCase(
    input=question,
    actual_output=result["answer"],
    expected_output=expected_answer,
    retrieval_context=[
        document["_source"]["text"]
        for document in result["sources"]
    ],
)
```

Then evaluate:

``` python
evaluate(
    test_cases=test_cases,
    metrics=metrics,
)
```

The exact metric imports and configuration should be verified against
the installed DeepEval version before running the full dataset.

------------------------------------------------------------------------

# 20. Important: preserve the source text

The current `ask()` result returns Elasticsearch documents.

For DeepEval, `retrieval_context` should normally be a list of strings
representing the retrieved chunks.

Therefore:

``` python
retrieval_context = [
    document["_source"]["text"]
    for document in result["sources"]
]
```

Do not pass only filenames.

Bad:

``` python
retrieval_context = [
    "In modern scientific terms.pdf",
    "Cosmic Origins Research Plan.pdf"
]
```

Good:

``` python
retrieval_context = [
    "actual retrieved chunk text...",
    "actual retrieved chunk text..."
]
```

The judge needs the evidence itself.

------------------------------------------------------------------------

# 21. Keep metadata separately

Although DeepEval primarily needs the text context, retain useful
metadata in the raw evaluation results.

For example:

``` json
{
  "source": "In modern scientific terms.pdf",
  "chunk_id": "In modern scientific terms_6",
  "score": 3.5111494
}
```

This makes debugging much easier.

The evaluation result should ideally preserve:

``` text
question
category
actual answer
expected answer
retrieved sources
retrieval scores
metric scores
metric reasons
```

This allows us to inspect why a particular test failed.

------------------------------------------------------------------------

# 22. Evaluation result interpretation

Do not report only:

``` text
Average score = 0.82
```

A useful evaluation report should contain:

``` text
Total questions: 10

Answer Relevancy:       0.87
Faithfulness:           0.91
Contextual Relevancy:   0.79
Contextual Precision:   0.76
Contextual Recall:      0.84
```

and, more importantly:

``` text
Worst cases:

Q04
Faithfulness: 0.42
Reason: Answer introduced claims not present in context.

Q07
Contextual Recall: 0.38
Reason: Retrieved chunks contained only part of the information needed.
```

The individual failures are more useful than the overall average.

------------------------------------------------------------------------

# 23. Baseline first, optimization second

The correct workflow is:

``` text
1. Freeze current RAG
        |
        v
2. Create evaluation dataset
        |
        v
3. Run baseline
        |
        v
4. Inspect weak cases
        |
        v
5. Change ONE component
        |
        v
6. Re-run evaluation
        |
        v
7. Compare against baseline
```

Do not change:

``` text
chunk size
embedding model
top_k
RRF
prompt
LLM
```

all at the same time.

Otherwise, you will not know which change caused the improvement or
regression.

------------------------------------------------------------------------

# 24. Example optimization experiments

Once the baseline exists, possible experiments include:

### Experiment A --- top_k

``` text
top_k = 3
top_k = 5
top_k = 8
```

Measure:

``` text
Contextual Relevancy
Contextual Recall
Faithfulness
Answer Relevancy
```

------------------------------------------------------------------------

### Experiment B --- chunk size

Compare different chunking configurations.

Measure whether larger or smaller chunks improve:

``` text
Contextual Recall
Contextual Relevancy
Faithfulness
```

------------------------------------------------------------------------

### Experiment C --- hybrid retrieval

Compare:

``` text
BM25
Vector
Hybrid/RRF
```

This is especially relevant to the LLM Zoomcamp evaluation methodology
because the course evaluates keyword, vector, and hybrid retrieval
quantitatively.

------------------------------------------------------------------------

### Experiment D --- prompt

Compare:

``` text
Current grounded prompt
```

against a carefully revised grounded prompt.

The prompt must still prevent unsupported answers.

------------------------------------------------------------------------

# 25. Evaluation versus monitoring

Evaluation and monitoring are related but different.

## Evaluation

Evaluation asks:

> Is the RAG system good?

It is usually run on a controlled dataset.

``` text
10 / 50 / 100 test questions
        |
        v
DeepEval
        |
        v
scores
```

## Monitoring

Monitoring asks:

> What is happening in the running application?

Examples:

-   request count
-   latency
-   errors
-   token usage
-   retrieved chunk count
-   production traces
-   user feedback

Monitoring is continuous.

Therefore:

``` text
Evaluation
    ↓
Establish quality baseline
    ↓
Monitoring
    ↓
Detect production changes
```

This is why evaluation should be completed before the final monitoring
layer.

------------------------------------------------------------------------

# 26. Evaluation versus Phoenix/Grafana

The project can eventually use both.

### DeepEval

Use for:

``` text
offline / controlled evaluation
```

Examples:

-   faithfulness
-   answer relevancy
-   contextual relevancy
-   contextual precision
-   contextual recall

### Phoenix

Use for:

``` text
LLM/RAG tracing and observability
```

Examples:

-   trace retrieval
-   inspect prompts
-   inspect generated answers
-   inspect latency
-   inspect spans

### Grafana

Use for:

``` text
application/system metrics
```

Examples:

-   request rate
-   latency
-   error rate
-   resource metrics

These tools are complementary rather than interchangeable.

------------------------------------------------------------------------

# 27. Recommended project progression

The recommended order is:

``` text
                CURRENT
                   |
                   v
          Existing RAG works
                   |
                   v
          Build 10-question set
                   |
                   v
            DeepEval baseline
                   |
                   v
        Diagnose weak components
                   |
                   v
       Improve retrieval/prompt
                   |
                   v
        Re-run DeepEval
                   |
                   v
        Freeze strong baseline
                   |
                   v
              FastAPI
                   |
                   v
             Streamlit
                   |
                   v
          Phoenix / Grafana
                   |
                   v
       Production-style monitoring
```

The exact placement of Phoenix/Grafana can evolve, but **do not skip the
evaluation baseline**.

------------------------------------------------------------------------

# 28. LLM-as-Judge limitations

LLM-as-a-Judge is powerful, but it is not perfect.

Potential problems include:

-   judge bias
-   verbosity bias
-   model-specific preferences
-   inconsistent reasoning
-   sensitivity to prompt wording
-   difficulty evaluating numerical correctness
-   correlated errors if the generator and judge are too similar

Therefore:

``` text
DeepEval score
      +
Reference answer
      +
Retrieved context
      +
Human inspection
```

should be considered together.

For numerical questions, use deterministic checks whenever practical.

For example, if the expected numerical result is:

``` text
42.5
```

a Python calculation can verify the numerical result independently of an
LLM judge.

------------------------------------------------------------------------

# 29. Version control

Commit the evaluation dataset and code:

``` text
eval/
├── README.md
├── questions.json
├── run_eval.py
└── test_eval.py
```

Do not commit secrets.

Be careful with evaluation results if they contain:

-   private documents
-   sensitive user questions
-   API responses
-   confidential information

For this project, the evaluation dataset is based on the project's own
PDFs, so it can normally be versioned with the project if those
documents are permitted to be redistributed.

------------------------------------------------------------------------

# 30. Reproducibility

Record at least:

``` text
date
git commit
LLM model
embedding model
top_k
chunking configuration
retrieval method
DeepEval version
judge model
dataset version
```

Example:

``` json
{
  "rag_model": "openai/gpt-oss-120b",
  "embedding_model": "Xenova/all-MiniLM-L6-v2",
  "retrieval": "hybrid_rrf",
  "top_k": 5,
  "dataset": "v1",
  "deepeval_version": "...",
  "evaluation_judge": "..."
}
```

This becomes extremely useful when comparing future experiments.

------------------------------------------------------------------------

# 31. Definition of success for the first milestone

The first evaluation milestone is complete when:

-   [ ] DeepEval is installed
-   [ ] 10 human-reviewed questions exist
-   [ ] Questions are grounded in the PDF corpus
-   [ ] Factual questions are included
-   [ ] Conceptual questions are included
-   [ ] Numerical/application questions are included where supported by
    the corpus
-   [ ] Unanswerable questions are included
-   [ ] Expected answers are human-verified
-   [ ] The existing `ask()` function is used by the evaluation
-   [ ] Retrieved chunks are passed as `retrieval_context`
-   [ ] Actual answers are captured
-   [ ] At least Faithfulness is measured
-   [ ] At least Answer Relevancy is measured
-   [ ] At least Contextual Relevancy is measured
-   [ ] Baseline scores are recorded
-   [ ] Failed cases can be inspected individually
-   [ ] No API keys are committed
-   [ ] The baseline is preserved before optimization

------------------------------------------------------------------------

# 32. Recommended first implementation

Do not begin with an overly complicated evaluation framework.

The first version should be:

``` text
eval/
├── README.md
├── questions.json
└── run_eval.py
```

After the first successful run, add:

``` text
results/
```

and later:

``` text
test_eval.py
```

The first goal is simply:

``` text
10 questions
     |
     v
existing ask()
     |
     v
DeepEval
     |
     v
baseline scores
```

Once this works reliably, expand it.

------------------------------------------------------------------------

# 33. Relationship to the LLM Zoomcamp project

This evaluation layer is an extension of the evaluation concepts taught
in the LLM Zoomcamp rather than a replacement for the underlying RAG
architecture.

The course evaluation work emphasizes creating a ground-truth dataset
and measuring retrieval quality rather than deciding which search method
is best by intuition.

This project extends that approach by adding DeepEval's LLM-as-a-Judge
metrics for both retrieval and generation.

The resulting evaluation architecture is:

``` text
                    RAG Evaluation
                         |
             +-----------+-----------+
             |                       |
             v                       v
       Retrieval quality       Generation quality
             |                       |
     +-------+-------+        +------+------+
     |       |       |        |             |
     v       v       v        v             v
Context   Context  Context  Faithfulness  Answer
Relevancy Precision Recall                 Relevancy
```

This gives a much more complete view of the system than looking only at
whether the final answer "sounds correct."

------------------------------------------------------------------------

# 34. Official references

DeepEval:

-   RAG Evaluation Quickstart
-   RAG Evaluation Guide
-   Faithfulness Metric
-   Answer Relevancy Metric
-   Contextual Relevancy Metric
-   Contextual Precision Metric
-   Contextual Recall Metric
-   Custom LLM Evaluation
-   DeepEval CLI

LLM Zoomcamp:

-   2026 Evaluation Homework
-   Evaluation module materials

Always check the installed DeepEval version and current official
documentation before copying an API example because the framework
evolves quickly.

------------------------------------------------------------------------

# 35. Final principle

The most important rule for this directory is:

> **Evaluate the RAG system you actually built, not a simplified version
> of it.**

The evaluation code should therefore call:

``` python
app.chat.service.ask()
```

and capture the real:

``` text
question
        |
        +--> retrieved chunks
        |
        +--> generated answer
```

Then DeepEval should evaluate those real outputs.

This preserves the integrity of the experiment and makes the evaluation
results useful when the project later moves to FastAPI, Streamlit,
Phoenix, Grafana, CI/CD, and production-style monitoring.
