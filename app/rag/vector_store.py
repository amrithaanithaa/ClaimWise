import chromadb
from sentence_transformers import SentenceTransformer

from app.rag.document_loader import load_policy_documents
from app.config import (CHROMA_PATH,COLLECTION_NAME, EMBEDDING_MODEL,)




def build_vector_store():
    documents = load_policy_documents()

    client = chromadb.PersistentClient(path=CHROMA_PATH)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    model = SentenceTransformer(EMBEDDING_MODEL)

    texts = []
    ids = []
    metadatas = []

    for index, document in enumerate(documents):
        text = (
            f"Policy: {document['policy_name']}\n"
            f"Section: {document['section']}\n\n"
            f"{document['content']}"
        )

        texts.append(text)
        ids.append(f"policy_section_{index}")

        metadatas.append({
            "policy_name": document["policy_name"],
            "section_number": document["section_number"],
            "section": document["section"],
            "source": document["source"],
        })

    embeddings = model.encode(texts).tolist()

    collection.upsert(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )

    print(f"Stored {len(texts)} policy sections.")
    print(f"Collection: {COLLECTION_NAME}")


if __name__ == "__main__":
    build_vector_store()