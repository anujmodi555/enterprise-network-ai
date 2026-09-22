import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def get_gemini_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not configured."
        )

    return genai.Client(api_key=api_key)


def ask_llm(question: str, network_context: str) -> str:
    client = get_gemini_client()

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.5-flash",
    )

    prompt = f"""
You are a network troubleshooting assistant.

Analyze the network information provided below.

Network information:
{network_context}

User question:
{question}

Rules:
- Only use information provided in the network context.
- Do not invent device telemetry.
- Clearly distinguish facts from possible causes.
- If the information is insufficient, say so.
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response.text