import logging
import os
import re
from pathlib import Path
from typing import Any

from google import genai

from .embeddings import embed_query, embed_document
from .vector_store import (
    insert_chunk,
    search_chunks,
)


logger = logging.getLogger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

KNOWLEDGE_DIR = (
    PROJECT_ROOT
    / "knowledge"
)


def normalize_text(text: str) -> str:
    """
    Normalize whitespace while preserving paragraph
    structure as much as possible.
    """

    text = text.replace(
        "\r\n",
        "\n",
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


def extract_title(
    text: str,
    fallback: str,
) -> str:
    """
    Extract the first Markdown H1 heading.
    """

    for line in text.splitlines():

        line = line.strip()

        if line.startswith("# "):
            return line[2:].strip()

    return fallback


def chunk_text(
    text: str,
    chunk_size: int = 180,
    overlap: int = 40,
) -> list[str]:
    """
    Split text into overlapping word-based chunks.

    chunk_size:
        Maximum number of words in a chunk.

    overlap:
        Number of words repeated between adjacent chunks.
    """

    if chunk_size <= 0:
        raise ValueError(
            "chunk_size must be greater than zero."
        )

    if overlap < 0:
        raise ValueError(
            "overlap cannot be negative."
        )

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size."
        )

    normalized = normalize_text(text)

    words = normalized.split()

    if not words:
        return []

    chunks: list[str] = []

    start = 0

    step = chunk_size - overlap

    while start < len(words):

        end = min(
            start + chunk_size,
            len(words),
        )

        chunk = " ".join(
            words[start:end]
        )

        chunks.append(chunk)

        if end == len(words):
            break

        start += step

    return chunks


def ingest_document(
    file_path: Path,
) -> int:
    """
    Read one Markdown document, chunk it, generate
    embeddings, and store the chunks in PostgreSQL.
    """

    text = file_path.read_text(
        encoding="utf-8"
    )

    title = extract_title(
        text=text,
        fallback=file_path.stem,
    )

    chunks = chunk_text(text)

    logger.info(
        "Ingesting %s: %s chunks",
        file_path.name,
        len(chunks),
    )

    for index, chunk in enumerate(chunks):

        embedding = embed_document(
            chunk
        )

        metadata = {
            "source_type": "markdown",
            "file_name": file_path.name,
        }

        insert_chunk(
            document_name=file_path.name,
            title=title,
            chunk_index=index,
            content=chunk,
            metadata=metadata,
            embedding=embedding,
        )

    return len(chunks)


def ingest_all_documents() -> int:
    """
    Ingest all Markdown documents from the knowledge directory.
    """

    files = sorted(
        KNOWLEDGE_DIR.glob("*.md")
    )

    if not files:
        raise RuntimeError(
            f"No Markdown documents found in {KNOWLEDGE_DIR}"
        )

    total_chunks = 0

    for file_path in files:

        total_chunks += ingest_document(
            file_path
        )

    return total_chunks


def retrieve_knowledge(
    question: str,
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """
    Convert a user question into an embedding and
    retrieve semantically similar knowledge chunks.
    """

    query_embedding = embed_query(
        question
    )

    return search_chunks(
        query_embedding=query_embedding,
        top_k=top_k,
    )


def build_context(
    results: list[dict[str, Any]],
) -> str:
    """
    Format retrieved chunks into context for Gemini.
    """

    if not results:
        return (
            "No relevant knowledge was retrieved "
            "from the knowledge base."
        )

    sections = []

    for index, result in enumerate(
        results,
        start=1,
    ):

        sections.append(
            f"""
SOURCE {index}
Document: {result["document_name"]}
Title: {result["title"]}
Similarity: {result["similarity"]:.4f}

Content:
{result["content"]}
""".strip()
        )

    return "\n\n".join(sections)


def ask_knowledge_question(
    question: str,
    top_k: int = 5,
) -> dict[str, Any]:
    """
    Retrieve relevant documentation and ask Gemini
    to produce a grounded answer.
    """

    results = retrieve_knowledge(
        question=question,
        top_k=top_k,
    )

    context = build_context(
        results
    )

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.7-flash",
    )

    client = genai.Client(
        api_key=api_key
    )

    prompt = f"""
You are an enterprise network knowledge assistant.

Answer the user's question using ONLY the
retrieved knowledge below.

Rules:
- Do not invent procedures or facts.
- Do not use knowledge that is not supported by the
  retrieved context.
- Clearly say when the retrieved information is insufficient.
- Distinguish documented guidance from your own reasoning.
- Mention the relevant source document names in the answer.

Retrieved knowledge:

{context}

User question:

{question}
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return {
        "answer": response.text or (
            "Gemini returned an empty response."
        ),
        "sources": [
            {
                "document_name": result[
                    "document_name"
                ],
                "title": result["title"],
                "similarity": result[
                    "similarity"
                ],
            }
            for result in results
        ],
    }