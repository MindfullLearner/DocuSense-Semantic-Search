
import os
from dotenv import load_dotenv
from google import genai

from search import search


# Load environment variables
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(BASE_DIR, ".env"))

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")

client = genai.Client(api_key=GEMINI_API_KEY)


def retrieve_context(query, top_k=5, strategy="fixed"):
    """Retrieve relevant document chunks."""

    results = search(
        query=query,
        top_k=top_k,
        strategy=strategy
    )

    return results


def build_context(results):
    """Construct context with source citation labels."""

    if not results:
        return ""

    context_parts = []

    for index, result in enumerate(results, start=1):
        metadata = result["metadata"]

        context_part = (
            f"[{index}]\n"
            f"Source: {metadata['source']}\n"
            f"Page: {metadata['page']}\n"
            f"Chunk: {metadata['chunk_index']}\n"
            f"Content:\n{result['text']}\n"
        )

        context_parts.append(context_part)

    return "\n---\n".join(context_parts)


def generate_answer(query, context):
    """Generate an answer using only the supplied context."""

    if not context.strip():
        return "I cannot answer because no relevant context was retrieved."

    prompt = f"""
You are DocuSense, a document-based question-answering assistant.

STRICT INSTRUCTIONS:
1. Answer the user's question using ONLY the supplied context.
2. Do not use outside knowledge or assumptions.
3. Do not invent facts or citations.
4. If the context does not contain enough information,
   clearly say that the available documents do not provide
   sufficient information.
5. Keep the answer clear and relevant.
6. Cite supporting sources using their reference labels,
   such as [1] or [2].

SUPPLIED CONTEXT:
{context}

USER QUESTION:
{query}

GROUNDED ANSWER:
"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt
    )

    if not response.text:
        return "The model did not return an answer."

    return response.text.strip()


def answer_question(query, top_k=3, strategy="fixed"):
    """Complete retrieval and answer-generation pipeline."""

    results = retrieve_context(
        query=query,
        top_k=top_k,
        strategy=strategy
    )

    print("\nDEBUG: Retrieved results count:", len(results))

    for index, result in enumerate(results, start=1):
        print(f"\nDEBUG Result {index}:")
        print("Text:", result["text"][:150])
        print("Metadata:", result["metadata"])
        print("Similarity:", result["similarity_score"])

    context = build_context(results)

    print("\nDEBUG: Context length:", len(context))

    answer = generate_answer(query=query, context=context)

    return {
        "question": query,
        "answer": answer,
        "sources": results
    }

if __name__ == "__main__":

    question = "What are foundation models?"

    print("\n========== DOCUSENSE RAG ==========")
    print("Question:", question)

    result = answer_question(
        query=question,
        top_k=3,
        strategy="fixed"
    )

    print("\n========== GENERATED ANSWER ==========")
    print(result["answer"])

    print("\n========== RETRIEVED SOURCES ==========")

    for index, source in enumerate(result["sources"], start=1):
        metadata = source["metadata"]

        print(f"\n[{index}]")
        print("Source:", metadata["source"])
        print("Page:", metadata["page"])
        print("Similarity:", source["similarity_score"])
