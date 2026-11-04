import sys

sys.path.insert(0, "src")

from search import search


# queries = [
#     "What is a foundation model and how is it trained?",
#     "What are the five key attributes of foundation models?",
#     "What societal consequences can foundation models have?"
# ]
queries = [
    "Why is evaluating foundation models difficult?",
    "What challenges arise when interpreting foundation model behavior?",
    "What economic risks can foundation models create?"
]

for query in queries:

    print("\n" + "=" * 70)
    print("QUERY:", query)

    results = search(query, top_k=3)

    for result in results:

        print("\nPAGE:", result["metadata"]["page"])
        print("SCORE:", result["similarity_score"])
        print("TEXT:", result["text"][:1400])