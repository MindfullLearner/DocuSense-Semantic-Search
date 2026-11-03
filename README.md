# DocuSense – Document-Based Semantic Search & RAG Question Answering

DocuSense is a Python-based document intelligence system that combines semantic search with Retrieval-Augmented Generation (RAG).

It extracts text from PDF documents, divides the text into chunks, generates semantic embeddings, and stores them in ChromaDB. Users can search across multiple documents using natural-language queries and retrieve relevant information with similarity scores and source metadata.

The RAG pipeline extends semantic search by using Google Gemini to generate grounded answers from retrieved document context, with source citations and similarity-based refusal for irrelevant questions.

## Features

### Document Processing
- Extract text from multiple PDF documents using PyMuPDF.
- Support fixed-size chunking with overlap.
- Support sentence-based chunking.
- Preserve source filename, page number, chunking strategy, and chunk index.

### Semantic Search
- Generate embeddings using Sentence Transformers.
- Use the `all-MiniLM-L6-v2` embedding model (384 dimensions).
- Store embeddings and metadata in ChromaDB.
- Perform natural-language semantic search.
- Retrieve top-k relevant chunks with cosine similarity scores.
- Compare retrieval results across chunking strategies.

### Retrieval-Augmented Generation (RAG)
- Retrieve relevant document chunks for user questions.
- Construct structured context with numbered source references.
- Generate grounded answers using Google Gemini.
- Restrict answer generation to supplied document context.
- Apply a configurable similarity threshold to filter irrelevant chunks.
- Refuse questions when no retrieved chunks meet the threshold.
- Validate generated citation labels against retrieved source references.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Embedding generation |
| all-MiniLM-L6-v2 | Pre-trained embedding model |
| ChromaDB | Persistent vector database |
| NumPy | Numerical operations |
| Google Gemini API | Grounded answer generation |
| google-genai | Gemini Python SDK |
| python-dotenv | Environment variable management |

## Project Structure

```text
DocuSense-Semantic-Search/
│
├── documents/
│   ├── google_ai.pdf
│   ├── nist_genai.pdf
│   └── stanford_foundation_models.pdf
│
├── src/
│   ├── ingest.py
│   ├── chunking.py
│   ├── vector_store.py
│   ├── search.py
│   └── rag.py
│
├── chroma_db/                  # Generated vector database
├── .env                        # Local API configuration (not committed)
├── .env.example                # Environment variable template
├── .gitignore
├── requirements.txt
├── README.md
├── CHUNKING_COMPARISON.md
└── EVAL_NOTES.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/DocuSense-Semantic-Search.git
cd DocuSense-Semantic-Search
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Gemini API

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.8-flash
```

Replace the placeholder with your own Gemini API key.

**Important:** Never commit your `.env` file or expose your API key publicly. The `.env` file is excluded through `.gitignore`.

### 5. Add PDF documents

Place your PDF files inside the `documents/` directory.

The project currently uses three example documents related to:
- Google Generative AI
- NIST Generative AI Risk Management
- Stanford Foundation Models

## How to Run

Run all commands from the project root.

### Step 1: Generate embeddings and populate ChromaDB

```bash
python .\src\vector_store.py
```

This process:

1. Extracts text from PDF documents.
2. Generates fixed-size and sentence-based chunks.
3. Generates embeddings using Sentence Transformers.
4. Stores chunks and metadata in separate ChromaDB collections.

Generated collections:

- `documents_fixed`
- `documents_sentence`

### Step 2: Perform semantic search

```bash
python .\src\search.py
```

The default example searches for:

```text
What are foundation models?
```

It retrieves the top matching chunks from the fixed-size collection.

### Step 3: Run the RAG question-answering pipeline

```bash
python .\src\rag.py
```

The RAG pipeline:

1. Receives a natural-language question.
2. Retrieves the top-k relevant document chunks.
3. Filters chunks using the configured similarity threshold.
4. Constructs context with numbered source references.
5. Sends the question and context to Google Gemini.
6. Generates a grounded answer.
7. Validates generated citation labels.
8. Displays the answer and retrieved source metadata.

### Step 4: Use the search function in another Python script

```python
import sys

sys.path.insert(0, "src")

from search import search

results = search(
    query="What are foundation models?",
    top_k=5,
    strategy="sentence"
)

for result in results:
    print("Source:", result["metadata"]["source"])
    print("Page:", result["metadata"]["page"])
    print("Similarity:", result["similarity_score"])
    print("Text:", result["text"])
```

Available strategies:

- `fixed`
- `sentence`

The `top_k` parameter controls how many relevant chunks are retrieved.

## RAG Architecture

```text
User Question
      |
      v
Query Embedding
      |
      v
ChromaDB Semantic Search
      |
      v
Retrieve Top-K Chunks
      |
      v
Similarity Threshold Filtering
      |
      +----------------------+
      |                      |
      v                      v
Relevant Chunks         No Relevant Chunks
      |                      |
      v                      v
Build Context            Refuse Answer
with Citations
      |
      v
Google Gemini
      |
      v
Grounded Answer
      |
      v
Citation Validation
      |
      v
Answer + Source References
```

## Similarity Threshold and Refusal

DocuSense uses a configurable similarity threshold:

```python
SIMILARITY_THRESHOLD = 0.50
```

Retrieved chunks below this threshold are excluded from the context.

If no retrieved chunks meet the threshold, the system refuses to answer rather than passing irrelevant information to Gemini.

The current threshold is an initial value evaluated using four test questions. It is not a universally optimal threshold.

## Citation Validation

Retrieved chunks are assigned numbered reference labels such as `[1]`, `[2]`, and `[3]`.

Gemini is instructed to use these references when supporting its answer.

DocuSense validates generated citation labels against the available retrieved source references. Answers containing invalid citation numbers are not accepted.

This validation checks reference existence, not whether every citation semantically supports its associated statement.

## Evaluation

The RAG pipeline was evaluated using two in-domain and two out-of-domain questions.

| Question | Category | Observed Result |
|---|---|---|
| What are foundation models? | In-domain | Grounded answer generated |
| What risks are associated with generative AI? | In-domain | Relevant answer generated |
| Who won the FIFA World Cup in 2018? | Out-of-domain | Correct refusal |
| What is the capital of Japan? | Out-of-domain | Correct refusal |

The evaluation demonstrated that the system can retrieve relevant information, generate context-based answers, and refuse questions when no retrieved chunks meet the configured threshold.

For detailed test outputs, retrieved sources, and observations, see `EVAL_NOTES.md`.

## Chunking Strategy Comparison

Two chunking strategies were evaluated using three search queries.

| Strategy | Total Chunks |
|---|---:|
| Fixed-size | 2,422 |
| Sentence-based | 2,577 |

The comparison evaluated retrieval relevance, similarity scores, and retrieved chunk context.

For detailed experimental results, see `CHUNKING_COMPARISON.md`.

## Similarity Scores

ChromaDB uses cosine distance for similarity search.

The implementation converts cosine distance into cosine similarity:

```python
similarity = 1 - distance
```

A higher similarity score indicates that the retrieved chunk is closer to the query in embedding space.

Similarity scores are not probabilities.

## Notes and Limitations

- The embedding model is downloaded and loaded locally through Sentence Transformers.
- An internet connection may be required when downloading the embedding model for the first time.
- ChromaDB stores generated data in the local `chroma_db/` directory.
- The vector database is excluded from Git and can be regenerated through the ingestion pipeline.
- Gemini API access is required for RAG answer generation.
- Semantic similarity alone does not guarantee that retrieved context contains a complete answer.
- Citation-label validation does not independently verify factual support.
- The current similarity threshold is an initial value and may require further evaluation.

## Author

Developed as part of the NeuroFive Generative AI & Prompt Engineering Internship.

## License

This project is intended for educational and internship purposes.