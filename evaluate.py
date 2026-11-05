
import argparse
import asyncio
import csv
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from openai import AsyncOpenAI

from ragas.llms import llm_factory
from ragas.embeddings.base import embedding_factory

from ragas.metrics.collections import (
    Faithfulness,
    AnswerRelevancy,
    ContextPrecision,
)


# --------------------------------------------------
# 1. Project configuration
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
SRC_DIR = BASE_DIR / "src"

sys.path.insert(0, str(SRC_DIR))

from rag import answer_question

load_dotenv(BASE_DIR / ".env")

DATASET_PATH = BASE_DIR / "evaluation_dataset.json"
OUTPUT_PATH = BASE_DIR / "evaluation_results.csv"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is missing from .env")


# --------------------------------------------------
# 2. Initialize Gemini evaluator
# --------------------------------------------------

evaluator_client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

evaluator_llm = llm_factory(
    GEMINI_MODEL,
    provider="openai",
    client=evaluator_client,
)

evaluator_embeddings = embedding_factory(
    "huggingface",
    model="sentence-transformers/all-MiniLM-L6-v2",
)


# --------------------------------------------------
# 3. Initialize Ragas metrics
# --------------------------------------------------

faithfulness_metric = Faithfulness(
    llm=evaluator_llm
)

answer_relevancy_metric = AnswerRelevancy(
    llm=evaluator_llm,
    embeddings=evaluator_embeddings,
)

context_precision_metric = ContextPrecision(
    llm=evaluator_llm
)


# --------------------------------------------------
# 4. Evaluate one question
# --------------------------------------------------

async def evaluate_question(item):

    question = item["question"]
    reference = item["reference"]

    print("\n" + "=" * 70)
    print("QUESTION:", question)

    # Generate answer using existing DocuSense RAG
    rag_result = answer_question(
        query=question,
        top_k=3,
    )

    response = rag_result["answer"]

    retrieved_contexts = [
        source["text"]
        for source in rag_result["sources"]
    ]

    print("\nGENERATED ANSWER:")
    print(response)

    print("\nRETRIEVED CONTEXTS:", len(retrieved_contexts))

    # Initialize scores
    faithfulness_score = None
    relevancy_score = None
    precision_score = None

    # Faithfulness
    if retrieved_contexts:
        try:
            faithfulness_result = await faithfulness_metric.ascore(
                user_input=question,
                response=response,
                retrieved_contexts=retrieved_contexts,
            )

            faithfulness_score = faithfulness_result.value

        except Exception as error:
            print(f"\nFaithfulness evaluation failed: {error}")

    else:
        print("Faithfulness skipped: No retrieved contexts.")

    # Answer Relevancy
    try:
        relevancy_result = await answer_relevancy_metric.ascore(
            user_input=question,
            response=response,
        )

        relevancy_score = relevancy_result.value

    except Exception as error:
        print(f"\nAnswer Relevancy evaluation failed: {error}")

    # Context Precision
    if retrieved_contexts:
        try:
            precision_result = await context_precision_metric.ascore(
                user_input=question,
                reference=reference,
                retrieved_contexts=retrieved_contexts,
            )

            precision_score = precision_result.value

        except Exception as error:
            print(f"\nContext Precision evaluation failed: {error}")

    else:
        print("Context Precision skipped: No retrieved contexts.")

    # Display scores
    print("\nEVALUATION SCORES:")
    print("Faithfulness:", faithfulness_score)
    print("Answer Relevancy:", relevancy_score)
    print("Context Precision:", precision_score)

    return {
        "question": question,
        "reference": reference,
        "response": response,
        "retrieved_contexts": json.dumps(
            retrieved_contexts,
            ensure_ascii=False,
        ),
        "faithfulness": faithfulness_score,
        "answer_relevancy": relevancy_score,
        "context_precision": precision_score,
    }


# --------------------------------------------------
# 5. Run evaluation dataset
# --------------------------------------------------

async def run_evaluation(limit=None):

    with open(DATASET_PATH, "r", encoding="utf-8") as file:
        dataset = json.load(file)

    selected_items = dataset[:limit] if limit else dataset

    print("\nTotal questions to evaluate:", len(selected_items))

    results = []

    for index, item in enumerate(selected_items, start=1):

        print(
            f"\nEvaluating question {index}/{len(selected_items)}"
        )

        try:
            result = await evaluate_question(item)
            results.append(result)

        except Exception as error:
            print("\nQuestion evaluation failed:", str(error))

            # Preserve failed question in results
            results.append({
                "question": item["question"],
                "reference": item["reference"],
                "response": "Evaluation failed during RAG generation.",
                "retrieved_contexts": "[]",
                "faithfulness": None,
                "answer_relevancy": None,
                "context_precision": None,
            })

    if not results:
        print("No evaluation results generated.")
        return

    # Save individual results
    with open(
        OUTPUT_PATH,
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        fieldnames = [
            "question",
            "reference",
            "response",
            "retrieved_contexts",
            "faithfulness",
            "answer_relevancy",
            "context_precision",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(results)

    # Calculate average scores
    print("\n" + "=" * 70)
    print("AVERAGE EVALUATION SCORES")

    for metric in [
        "faithfulness",
        "answer_relevancy",
        "context_precision",
    ]:

        valid_scores = [
            result[metric]
            for result in results
            if result[metric] is not None
        ]

        if valid_scores:
            average = sum(valid_scores) / len(valid_scores)

            print(
                f"{metric}: {average:.4f} "
                f"({len(valid_scores)}/{len(results)} successful)"
            )

        else:
            print(f"{metric}: No valid scores")

    print("\nResults saved to:", OUTPUT_PATH)


# --------------------------------------------------
# 6. Main entry point
# --------------------------------------------------

if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Evaluate DocuSense using Ragas."
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=1,
        help="Number of questions to evaluate (default: 1).",
    )

    args = parser.parse_args()

    if args.limit <= 0:
        parser.error("--limit must be greater than zero.")

    asyncio.run(run_evaluation(args.limit))
