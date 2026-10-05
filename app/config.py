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