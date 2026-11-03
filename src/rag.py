
from search import search


def retrieve_context(query, top_k=5, strategy="fixed"):
    """
    Retrieve relevant document chunks for a user query.
    """
    results = search(
        query=query,
        top_k=top_k,
        strategy=strategy
    )

    return results


def build_context(results):
    """
    Convert retrieved chunks into structured context
    with citation labels.
    """

    if not results:
        return ""

    context_parts = []

    for index, result in enumerate(results, start=1):
        metadata = result["metadata"]

        source = metadata["source"]
        page = metadata["page"]
        chunk_index = metadata["chunk_index"]
        similarity = result["similarity_score"]
        text = result["text"]

        context_part = (
            f"[{index}]\n"
            f"Source: {source}\n"
            f"Page: {page}\n"
            f"Chunk: {chunk_index}\n"
            f"Similarity: {similarity}\n"
            f"Content:\n{text}\n"
        )

        context_parts.append(context_part)

    return "\n---\n".join(context_parts)


if __name__ == "__main__":

    query = "What are foundation models?"

    print("\n========== RETRIEVING CONTEXT ==========")

    results = retrieve_context(
        query=query,
        top_k=3,
        strategy="fixed"
    )

    context = build_context(results)

    print("\nUser Question:", query)
    print("\n========== CONSTRUCTED CONTEXT ==========")
    print(context)

    print("\nTotal retrieved chunks:", len(results))
