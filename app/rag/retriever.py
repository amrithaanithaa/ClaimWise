
import chromadb
from sentence_transformers import SentenceTransformer

from app.config import (
    CHROMA_PATH,
    COLLECTION_NAME,
    EMBEDDING_MODEL,
)

# Initialize the database and embedding model once.
_client = chromadb.PersistentClient(
    path=str(CHROMA_PATH)
)

_collection = _client.get_collection(
    name=COLLECTION_NAME
)

_model = SentenceTransformer(EMBEDDING_MODEL)


def retrieve_policy_sections(
    query: str,
    top_k: int = 3,
    policy_name: str | None = None,
    max_distance: float | None = None,
) -> dict:
    """
    Retrieve relevant policy sections.

    Args:
        query: User's question.
        top_k: Maximum number of sections to retrieve.
        policy_name: Optional policy-name filter.
        max_distance: Optional maximum ChromaDB distance.
                      Lower distances are closer matches.
                      None disables distance filtering.

    Returns:
        ChromaDB results, including documents, metadata,
        distances, and IDs.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty.")

    if top_k < 1:
        raise ValueError("top_k must be at least 1.")

    if max_distance is not None and max_distance < 0:
        raise ValueError("max_distance cannot be negative.")

    # Embed the user's question.
    query_embedding = _model.encode(
        query.strip()
    ).tolist()

    # Prepare the vector search.
    search_options = {
        "query_embeddings": [query_embedding],
        "n_results": top_k,
        "include": [
            "documents",
            "metadatas",
            "distances",
        ],
    }

    # Filter by policy when one is identified.
    if policy_name:
        search_options["where"] = {
            "policy_name": policy_name
        }

    results = _collection.query(**search_options)

    # Optional post-retrieval distance filtering.
    if max_distance is not None:
        documents = results.get("documents", [[]])[0] or []
        metadatas = results.get("metadatas", [[]])[0] or []
        distances = results.get("distances", [[]])[0] or []
        ids = results.get("ids", [[]])[0] or []

        kept_indices = [
            index
            for index, distance in enumerate(distances)
            if distance <= max_distance
        ]

        # Preserve the original ChromaDB result structure.
        for field, values in [
            ("documents", documents),
            ("metadatas", metadatas),
            ("distances", distances),
            ("ids", ids),
        ]:
            results[field] = [[
                values[index] for index in kept_indices
            ]]

    return results


if __name__ == "__main__":
    test_questions = [
        (
            "What is the maternity waiting period under Health Secure Plus?",
            "Health Secure Plus",
        ),
        (
            "Is drunk driving covered under Motor Protect Comprehensive?",
            "Motor Protect Comprehensive",
        ),
        (
            "What is covered for hospitalization?",
            None,
        ),
    ]

    for query, policy_name in test_questions:
        results = retrieve_policy_sections(
            query=query,
            top_k=5,
            policy_name=policy_name,
            # Keep filtering disabled for the initial test.
            max_distance=None,
        )

        print("\n" + "=" * 70)
        print(f"Question: {query}")
        print(f"Policy filter: {policy_name or 'All policies'}")

        documents = results.get("documents", [[]])[0] or []
        metadatas = results.get("metadatas", [[]])[0] or []
        distances = results.get("distances", [[]])[0] or []

        if not documents:
            print("No matching sections found.")
            continue

        for index, (document, metadata, distance) in enumerate(
            zip(documents, metadatas, distances),
            start=1,
        ):
            print("-" * 60)
            print(f"Rank: {index}")
            print(f"Distance: {distance:.4f}")
            print(f"Policy: {metadata.get('policy_name')}")
            print(
                f"Section: {metadata.get('section_number')} - "
                f"{metadata.get('section')}"
            )
            print(f"Source: {metadata.get('source')}")
            print(f"Content: {document[:200]}...")
