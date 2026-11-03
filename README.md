# DocuSense – Document Ingestion, Chunking & Semantic Search Pipeline

DocuSense is a Python-based semantic search system that extracts text from PDF documents, divides the text into chunks, generates embeddings, and stores them in ChromaDB.

It allows users to search across multiple documents using natural-language queries and retrieves the most relevant text chunks with similarity scores and source metadata.

## Features

- Extract text from multiple PDF documents using PyMuPDF.
- Support two chunking strategies:
  - Fixed-size chunking with overlap.
  - Sentence-based chunking.
- Generate text embeddings using Sentence Transformers.
- Use the `all-MiniLM-L6-v2` embedding model (384 dimensions).
- Store document embeddings and metadata in ChromaDB.
- Perform semantic search using natural-language queries.
- Retrieve top-k relevant results with cosine similarity scores.
- Preserve source filename, page number, chunking strategy, and chunk index metadata.
- Compare retrieval results across different chunking strategies.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| PyMuPDF | PDF text extraction |
| Sentence Transformers | Text embedding generation |
| all-MiniLM-L6-v2 | Pre-trained embedding model |
| ChromaDB | Persistent vector database |
| NumPy | Numerical operations |

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
│   └── search.py
│
├── chroma_db/                 # Generated vector database
├── .gitignore
├── .env.example
├── requirements.txt
├── README.md
└── CHUNKING_COMPARISON.md
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

### 4. Add PDF documents

Place your PDF files inside the `documents/` directory.

The project currently uses three example documents related to Google Generative AI, NIST Generative AI risk management, and Stanford foundation models.

## How to Run

### Step 1: Generate embeddings and populate ChromaDB

Run the following command from the project root:

```bash
python .\src\vector_store.py
```

This process:

1. Extracts text from the PDF documents.
2. Generates fixed-size and sentence-based chunks.
3. Generates embeddings using Sentence Transformers.
4. Stores the chunks and metadata in two separate ChromaDB collections.

The generated collections are:

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

It retrieves the top three matching chunks from the fixed-size collection.

### Step 3: Use the search function

The search function can also be imported into another Python script:

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

The `top_k` parameter controls how many relevant chunks are returned.

## Semantic Search Workflow

```text
PDF Documents
      |
      v
Text Extraction (PyMuPDF)
      |
      v
Text Chunking
   /       \
Fixed     Sentence
   \       /
      |
      v
Embedding Generation
(Sentence Transformers)
      |
      v
ChromaDB Vector Storage
      |
      v
User Search Query
      |
      v
Query Embedding
      |
      v
Similarity Search
      |
      v
Top-K Relevant Results
```

## Chunking Strategy Comparison

Two chunking strategies were evaluated using three search queries.

| Strategy | Total Chunks |
|---|---:|
| Fixed-size | 2,422 |
| Sentence-based | 2,577 |

The comparison evaluated retrieval relevance, similarity scores, and the context of retrieved chunks.

For detailed experimental results and observations, see [CHUNKING_COMPARISON.md](CHUNKING_COMPARISON.md).

## Similarity Scores

ChromaDB uses cosine distance for similarity search.

The implementation converts cosine distance into cosine similarity using:

```python
similarity = 1 - distance
```

A higher similarity score indicates that the retrieved chunk is closer to the query in the embedding space. Similarity scores are not probabilities.

## Notes

- The embedding model is downloaded and loaded locally through Sentence Transformers.
- An internet connection may be required the first time the model is downloaded.
- ChromaDB stores its generated data in the local `chroma_db/` directory.
- The vector database is excluded from Git using `.gitignore` and can be regenerated by running the ingestion pipeline.
- No Gemini API key is required.

## Author

Developed as part of the NeuroFive Generative AI & Prompt Engineering Internship.

## License

This project is intended for educational and internship purposes.