from pathlib import Path
import re

from app.config import POLICY_DOCUMENT_PATH


def load_policy_documents():
    documents = []

    for file_path in POLICY_DOCUMENT_PATH.glob("*.txt"):
        text = file_path.read_text(encoding="utf-8")

        policy_name = file_path.stem.replace("_", " ")

        sections = re.split(
            r"\n(?=\d+\.\s+.+)",
            text
        )

        for section in sections:
            section = section.strip()

            if not section:
                continue

            match = re.match(
                r"(\d+)\.\s+(.+?)(?:\n|$)",
                section
            )

            if not match:
                continue

            section_number = match.group(1)
            section_title = match.group(2).strip()
            content = section[match.end():].strip()

            documents.append({
                "policy_name": policy_name,
                "section_number": section_number,
                "section": section_title,
                "content": content,
                "source": file_path.name,
            })

    return documents