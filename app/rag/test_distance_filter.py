
# from app.rag.retriever import retrieve_policy_sections

# results = retrieve_policy_sections(
#     query="What is the maternity waiting period under Health Secure Plus?",
#     top_k=5,
#     policy_name="Health Secure Plus",
#     max_distance=0.7,
# )

# print("Distances:")
# print(results["distances"])

# print("\nRetrieved policy sections:")
# for metadata in results["metadatas"][0]:
#     print(
#         metadata["policy_name"],
#         "| Section", metadata["section_number"],
#         "-", metadata["section"],
#     )




from app.rag.retriever import retrieve_policy_sections

test_cases = [
    {
        "question": (
            "Is drunk driving covered under "
            "Motor Protect Comprehensive?"
        ),
        "policy_name": "Motor Protect Comprehensive",
    },
    {
        "question": "What is covered for hospitalization?",
        "policy_name": None,
    },
]

for test in test_cases:
    question = test["question"]
    policy_name = test["policy_name"]

    print("\n" + "=" * 70)
    print(f"Question: {question}")
    print(f"Policy filter: {policy_name or 'All policies'}")

    results = retrieve_policy_sections(
        query=question,
        top_k=5,
        policy_name=policy_name,
        max_distance=0.7,
    )

    documents = results["documents"][0] or []
    metadatas = results["metadatas"][0] or []
    distances = results["distances"][0] or []

    if not documents:
        print("No sections passed the distance filter.")
        continue

    for metadata, distance in zip(metadatas, distances):
        print(
            f"Distance: {distance:.4f} | "
            f"{metadata['policy_name']} | "
            f"Section {metadata['section_number']}: "
            f"{metadata['section']}"
        )
