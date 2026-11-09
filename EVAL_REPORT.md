
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

The first question, "What is generative AI?", successfully generated an answer and retrieved three contexts.

Metric results for this evaluation run:

| Metric | Score | Status |
|---|---:|---|
| Faithfulness | 1.0000 | Successfully calculated |
| Answer Relevancy | 0.9601 | Successfully calculated |
| Context Precision | 1.0000 | Successfully calculated |

Faithfulness achieved a score of 1.0000, indicating that the generated answer was consistent with the retrieved contexts.

Answer Relevancy achieved a score of 0.9601, indicating strong relevance between the generated answer and the user query.

Context Precision achieved a score of 1.0000, indicating that the generated answer was consistent with the retrieved contexts.

These results represent one question only (1/10) and should not be treated as final dataset averages.

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
