import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DATABASE_PATH = Path(
    os.getenv("DATABASE_PATH", "data/claimwise.db")
)

DATA_PATH = Path(
    os.getenv("DATA_PATH", "data")
)

POLICY_DOCUMENT_PATH = Path(
    os.getenv("POLICY_DOCUMENT_PATH", "data/policy_documents")
)

CHROMA_PATH = Path(
    os.getenv("CHROMA_PATH", "chroma_db")
)

# Collection name must be a string
COLLECTION_NAME = os.getenv(
    "COLLECTION_NAME",
    "claimwise_policies"
)

# Embedding model name must be a string
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)

#OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")