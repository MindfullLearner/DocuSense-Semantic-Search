
# RAG Evaluation & Guardrails Report

## 1. Project Overview

This project evaluates the DocuSense Retrieval-Augmented Generation (RAG) pipeline and implements security guardrails.

The evaluation focuses on:
- Faithfulness
- Answer Relevancy
- Context Precision
- Prompt injection detection
- Personally Identifiable Information (PII) detection and redaction

## 2. Evaluation Dataset

A dataset of 10 question-reference pairs was created using three source documents:

1. Google AI documentation
2. NIST Generative AI Profile
3. Stanford Foundation Models documentation

The dataset covers generative AI, prompt engineering, NIST risk management, and foundation models.

## 3. Evaluation Metrics

### Faithfulness
Measures whether generated answers are supported by the retrieved context.

### Answer Relevancy
Measures how relevant the generated answer is to the user's question.

### Context Precision
Measures whether relevant retrieved chunks are ranked above irrelevant chunks.

## 4. Evaluation Results

Evaluation was implemented using Ragas 0.4.3.

The first evaluation question successfully generated an answer and retrieved three contexts.

However, metric calculation was interrupted by Gemini API limitations:

- Faithfulness: Incomplete evaluator response due to max_tokens limit.
- Answer Relevancy: Not calculated due to HTTP 429 rate limit.
- Context Precision: Not calculated due to HTTP 429 rate limit.

Therefore, numerical scores and averages remain pending. These failures are not zero scores.

Results are saved in `evaluation_results.csv`.

## 5. Guardrails Implementation

The `guardrails.py` module implements:

- Prompt injection detection using regular expressions.
- Email address detection and redaction.
- Pakistani mobile number detection and redaction.
- Combined scanning through `scan_text()`.

PII is replaced with:
- `[REDACTED_EMAIL]`
- `[REDACTED_PHONE]`

## 6. Guardrails Test Results

Automated tests were executed using pytest.

| Test | Result |
|---|---|
| Prompt injection detection | Passed |
| Safe text detection | Passed |
| Email redaction | Passed |
| Phone redaction | Passed |
| Combined scanning | Passed |
| Text without PII | Passed |

Total: 6 passed.

## 7. Identified RAG Weakness

Dense vector search can retrieve chunks with high semantic similarity that do not necessarily contain the exact information required to answer a question.

For example, a broad query about foundation models may retrieve introductory content instead of the specific chunk containing their detailed definition.

### Proposed Fix

Implement hybrid retrieval by combining:
- Dense vector search
- BM25 keyword search
- A reranking model to improve the final ranking of retrieved chunks

This can improve retrieval precision and provide more useful context to the generation model.

## 8. Limitations

- Regex-based prompt injection detection cannot identify every possible attack.
- PII detection currently focuses on email addresses and common Pakistani mobile number formats.
- Citation validation checks reference-label validity but does not verify semantic support for every claim.
- Numerical Ragas evaluation scores are pending successful API requests.

## 9. Conclusion

The project successfully implements a 10-question evaluation dataset, a Ragas-based evaluation pipeline, and automated security guardrails.

The guardrails passed all six automated tests. The evaluation pipeline generated an answer and retrieved contexts, but metric calculation requires a successful evaluator API run.
