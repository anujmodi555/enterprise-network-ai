import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


def get_gemini_client() -> genai.Client:

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured."
        )

    return genai.Client(
        api_key=api_key
    )


def get_embedding_model() -> str:

    return os.getenv(
        "GEMINI_EMBEDDING_MODEL",
        "gemini-embedding-001",
    )


def get_embedding_dimensions() -> int:

    return int(
        os.getenv(
            "EMBEDDING_DIMENSIONS",
            "1536",
        )
    )


def embed_text(
    text: str,
    task_type: str,
) -> list[float]:

    client = get_gemini_client()

    response = client.models.embed_content(
        model=get_embedding_model(),
        contents=text,
        config=types.EmbedContentConfig(
            task_type=task_type,
            output_dimensionality=(
                get_embedding_dimensions()
            ),
        ),
    )

    if not response.embeddings:
        raise RuntimeError(
            "Gemini returned no embeddings."
        )

    values = response.embeddings[0].values

    if not values:
        raise RuntimeError(
            "Gemini returned an empty embedding."
        )

    return list(values)


def embed_document(
    text: str,
) -> list[float]:

    return embed_text(
        text=text,
        task_type="RETRIEVAL_DOCUMENT",
    )


def embed_query(
    text: str,
) -> list[float]:

    return embed_text(
        text=text,
        task_type="RETRIEVAL_QUERY",
    )