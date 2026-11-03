# Chunking Strategy Comparison

## 1. Objective

The purpose of this experiment is to compare two text chunking strategies for a semantic search pipeline:

- Fixed-size chunking
- Sentence-based chunking

Both strategies were evaluated using the same three queries and the same embedding model to observe their impact on semantic retrieval.

## 2. Experimental Setup

| Component | Configuration |
|---|---|
| Source documents | 3 PDF documents |
| Total extracted pages | 289 |
| Embedding model | all-MiniLM-L6-v2 |
| Embedding dimensions | 384 |
| Vector database | ChromaDB |
| Similarity metric | Cosine similarity |
| Fixed chunk size | 500 characters |
| Fixed chunk overlap | 50 characters |
| Sentence chunk size | Approximately 500 characters |
| Results per query | Top 3 |

## 3. Chunking Strategies

### Fixed-size Chunking

Text is divided into chunks of approximately 500 characters, with a 50-character overlap between consecutive chunks.

**Advantages:**
- Consistent chunk sizes.
- Overlap helps preserve context between neighboring chunks.
- Predictable chunking behavior.

**Limitations:**
- May split sentences across chunks.
- A chunk may contain parts of multiple topics.

### Sentence-based Chunking

Text is divided into groups of complete sentences, targeting approximately 500 characters per chunk.

**Advantages:**
- Preserves sentence boundaries.
- Can produce more coherent text segments.
- Reduces the chance of splitting a sentence.

**Limitations:**
- Chunk lengths can vary.
- A single long sentence can exceed the target size.

## 4. Chunk Generation Results

| Strategy | Total Chunks |
|---|---:|
| Fixed-size | 2,422 |
| Sentence-based | 2,577 |

Sentence-based chunking generated 155 more chunks than fixed-size chunking.

## 5. Queries and Retrieval Results

Both strategies were tested with the same three queries. Each search returned its top three results.

### Query 1: Foundation Models

**Query:** What are foundation models and how are they used?

| Strategy | Top Result Source | Page | Similarity |
|---|---|---:|---:|
| Fixed-size | stanford_foundation_models.pdf | 12 | 0.7549 |
| Sentence-based | stanford_foundation_models.pdf | 127 | 0.7835 |

**Observation:** Sentence-based chunking achieved a higher top similarity score. Both strategies retrieved content from the Stanford foundation models document, although they selected different sections.

### Query 2: Generative AI Risks

**Query:** What risks and challenges should organizations consider when using generative AI?

| Strategy | Top Result Source | Page | Similarity |
|---|---|---:|---:|
| Fixed-size | google_ai.pdf | 10 | 0.6265 |
| Sentence-based | nist_genai.pdf | 51 | 0.6071 |

**Observation:** Fixed-size chunking achieved a slightly higher similarity score. However, sentence-based chunking ranked the NIST document's governance and risk-management section first, which was directly relevant to the query.

### Query 3: Prompt Quality

**Query:** What techniques can improve prompts and the quality of generative AI outputs?

| Strategy | Top Result Source | Page | Similarity |
|---|---|---:|---:|
| Fixed-size | google_ai.pdf | 3 | 0.7148 |
| Sentence-based | google_ai.pdf | 3 | 0.7148 |

**Observation:** Both strategies retrieved the same top result with the same similarity score. The retrieved section directly discusses prompt engineering.

## 6. Overall Comparison

| Evaluation Aspect | Fixed-size | Sentence-based |
|---|---|---|
| Total chunks | 2,422 | 2,577 |
| Context preservation | Uses overlap | Preserves sentence boundaries |
| Foundation models query | Relevant Stanford content | Relevant Stanford content |
| Generative AI risks query | General responsible AI content ranked first | NIST risk-management content ranked first |
| Prompt quality query | Relevant Google content | Same relevant Google content |
| Chunk length | More consistent | Variable |

## 7. Conclusion

Both chunking strategies successfully supported semantic search across the three PDF documents.

Sentence-based chunking produced more chunks and preserved complete sentences, which can improve the coherence of retrieved text. It also retrieved a directly relevant NIST risk-management section for the second query.

Fixed-size chunking produced fewer chunks and achieved higher top similarity scores for the second query. However, its highest-ranked result was less directly focused on generative AI risk management.

Neither strategy was consistently better across all queries. The experiment suggests that the effectiveness of a chunking strategy depends on the content and the type of query.

For this small experiment, sentence-based chunking showed useful advantages in contextual coherence, while fixed-size chunking provided more consistent chunk sizes and overlap-based context preservation.

## 8. Limitations

- Only three queries were used for evaluation.
- Retrieval quality was assessed through the returned text and similarity scores rather than a large human-evaluated benchmark.
- Cosine similarity scores measure vector similarity and are not probabilities or direct measures of answer correctness.
- Results may vary with different embedding models, chunk sizes, overlap settings, and queries.

A larger evaluation with more queries and human relevance judgments would provide stronger evidence about which strategy performs better.