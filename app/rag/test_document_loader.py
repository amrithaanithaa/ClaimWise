from app.rag.document_loader import load_policy_documents


documents = load_policy_documents()

print("Total sections:", len(documents))

for document in documents[:5]:
    print("\n" + "=" * 60)
    print("Policy:", document["policy_name"])
    print("Section:", document["section"])
    print("Source:", document["source"])
    print("Content:", document["content"])