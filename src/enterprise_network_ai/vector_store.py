import json
import os
from typing import Any

import psycopg
from pgvector import Vector
from pgvector.psycopg import register_vector
from dotenv import load_dotenv


load_dotenv()


def get_database_url() -> str:

    database_url = os.getenv(
        "DATABASE_URL"
    )

    if not database_url:
        raise RuntimeError(
            "DATABASE_URL is not configured."
        )

    return database_url


def insert_chunk(
    document_name: str,
    title: str,
    chunk_index: int,
    content: str,
    metadata: dict[str, Any],
    embedding: list[float],
) -> None:

    vector = Vector(
        embedding
    )

    with psycopg.connect(
        get_database_url()
    ) as conn:

        register_vector(conn)

        conn.execute(
            """
            INSERT INTO knowledge_chunks (
                document_name,
                title,
                chunk_index,
                content,
                metadata,
                embedding
            )
            VALUES (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
            )
            ON CONFLICT (
                document_name,
                chunk_index
            )
            DO UPDATE SET
                title = EXCLUDED.title,
                content = EXCLUDED.content,
                metadata = EXCLUDED.metadata,
                embedding = EXCLUDED.embedding
            """,
            (
                document_name,
                title,
                chunk_index,
                content,
                json.dumps(metadata),
                vector,
            ),
        )

        conn.commit()


def search_chunks(
    query_embedding: list[float],
    top_k: int = 5,
) -> list[dict[str, Any]]:

    if top_k < 1:
        raise ValueError(
            "top_k must be at least 1."
        )

    vector = Vector(
        query_embedding
    )

    with psycopg.connect(
        get_database_url()
    ) as conn:

        register_vector(conn)

        rows = conn.execute(
            """
            SELECT
                id,
                document_name,
                title,
                chunk_index,
                content,
                metadata,
                1 - (
                    embedding <=> %s
                ) AS similarity
            FROM knowledge_chunks
            ORDER BY embedding <=> %s
            LIMIT %s
            """,
            (
                vector,
                vector,
                top_k,
            ),
        ).fetchall()

    results = []

    for row in rows:

        results.append(
            {
                "id": row[0],
                "document_name": row[1],
                "title": row[2],
                "chunk_index": row[3],
                "content": row[4],
                "metadata": row[5],
                "similarity": float(row[6]),
            }
        )

    return results