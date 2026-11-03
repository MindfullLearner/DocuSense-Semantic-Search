# DocuSense – RAG Evaluation Notes

## 1. Overview

This document records the evaluation of the DocuSense Retrieval-Augmented Generation (RAG) pipeline.

The system retrieves relevant document chunks from ChromaDB and uses Google Gemini to generate answers grounded in the retrieved context.

## 2. Evaluation Configuration

| Setting | Value |
|---|---|
| Embedding model | all-MiniLM-L6-v2 |
| Vector database | ChromaDB |
| LLM provider | Google Gemini |
| Chunking strategy | Fixed-size |
| Chunk size | 500 characters |
| Chunk overlap | 50 characters |
| Top-K retrieval | 3 |
| Similarity threshold | 0.50 |

The system refuses to generate an answer when none of the retrieved chunks meets the similarity threshold.

## 3. Test Cases

### Test 1: Foundation Models

**Question:** What are foundation models?

**Type:** In-domain

**Retrieved sources:**

| Source | Page | Similarity |
|---|---:|---:|
| stanford_foundation_models.pdf | 12 | 0.7974 |
| stanford_foundation_models.pdf | 127 | 0.7661 |
| stanford_foundation_models.pdf | 16 | 0.7553 |

**Generated answer:**

The documents describe foundation models as having a one model–many models nature and identify architectural characteristics such as expressivity and scalability.

The model also acknowledged that the retrieved context did not provide a complete or direct definition.

**Citations:** [2], [3]

**Result:** Answer generated using retrieved context. The answer was partially informative but did not provide a complete definition.

### Test 2: Generative AI Risks

**Question:** What risks are associated with generative AI?

**Type:** In-domain

**Retrieved sources:**

| Source | Page | Similarity |
|---|---:|---:|
| nist_genai.pdf | 60 | 0.6605 |
| nist_genai.pdf | 5 | 0.6293 |
| nist_genai.pdf | 7 | 0.6038 |

**Generated answer:**

The model identified several risks, including:

- Technical and model risks
- Confabulation
- Dangerous or violent recommendations
- Data privacy
- Value chain and component integration
- Harmful outcomes
- Bias

**Citations:** [1], [2], [3]

**Result:** Relevant answer generated using retrieved document context.

### Test 3: FIFA World Cup

**Question:** Who won the FIFA World Cup in 2018?

**Type:** Out-of-domain

**Retrieved chunks:** 3

**Relevant chunks after threshold filtering:** 0

**Generated response:**

"I cannot answer this question because the available documents do not contain sufficiently relevant information."

**Citations:** None

**Result:** Correctly refused because no retrieved chunk met the similarity threshold.

### Test 4: Capital of Japan

**Question:** What is the capital of Japan?

**Type:** Out-of-domain

**Retrieved chunks:** 3

**Relevant chunks after threshold filtering:** 0

**Generated response:**

"I cannot answer this question because the available documents do not contain sufficiently relevant information."

**Citations:** None

**Result:** Correctly refused because no retrieved chunk met the similarity threshold.

## 4. Evaluation Summary

| Test | Question Type | Expected Behavior | Observed Behavior |
|---|---|---|---|
| 1 | In-domain | Generate grounded answer | Answer generated |
| 2 | In-domain | Generate grounded answer | Answer generated |
| 3 | Out-of-domain | Refuse to answer | Correct refusal |
| 4 | Out-of-domain | Refuse to answer | Correct refusal |

## 5. Observations

1. The RAG pipeline successfully retrieves document chunks from ChromaDB.
2. Similarity threshold filtering prevents irrelevant retrieved chunks from being passed to Gemini.
3. Gemini generates answers using the supplied document context.
4. The model uses citation labels to identify supporting retrieved chunks.
5. Out-of-domain questions are rejected when no retrieved chunks meet the configured threshold.
6. The foundation-model question produced an incomplete answer, showing that retrieval relevance alone does not guarantee answer completeness.

## 6. Limitations and Future Improvements

- Evaluate more questions to improve confidence in the similarity threshold.
- Experiment with different threshold values.
- Improve retrieval quality and context construction.
- Validate generated citation labels against retrieved source references.
- Test additional chunking strategies and compare answer quality.
- Improve answer completeness while maintaining strict grounding.

## 7. Conclusion

The DocuSense RAG pipeline successfully combines semantic retrieval, ChromaDB, similarity threshold filtering, and Google Gemini answer generation.

The four evaluation tests demonstrate that the system can generate document-grounded answers for in-domain questions and refuse questions when the retrieved context is insufficient.

The current evaluation provides an initial validation of the RAG implementation. Further testing is recommended to improve retrieval accuracy, citation reliability, and answer completeness.