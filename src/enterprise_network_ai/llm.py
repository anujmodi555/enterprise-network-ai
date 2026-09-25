import logging
import os
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types

from .tools import TOOL_DECLARATIONS, TOOL_REGISTRY


load_dotenv()

logger = logging.getLogger(__name__)

MAX_TOOL_ROUNDS = 5


def get_gemini_client() -> genai.Client:
    """
    Create a Gemini API client using the configured API key.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable is not configured."
        )

    return genai.Client(api_key=api_key)


def execute_tool(
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute a tool from the approved tool registry.

    The model chooses the tool name and arguments,
    but this application controls which Python functions
    are actually executable.
    """

    tool = TOOL_REGISTRY.get(tool_name)

    if not tool:
        return {
            "success": False,
            "error": f"Unknown tool: {tool_name}",
        }

    try:
        result = tool(**arguments)

        return {
            "success": True,
            "data": result,
        }

    except (TypeError, ValueError, KeyError) as exc:
        logger.warning(
            "Tool execution failed: tool=%s error=%s",
            tool_name,
            exc,
        )

        return {
            "success": False,
            "error": str(exc),
        }


def ask_network_assistant(
    question: str,
) -> str:
    """
    Ask Gemini a network troubleshooting question
    and allow it to call approved network tools.
    """

    client = get_gemini_client()

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-2.5-flash",
    )

    system_prompt = """
You are an enterprise network troubleshooting assistant.

You have access to read-only network diagnostic tools.

Rules:
- Use tools when current network information is required.
- Do not invent telemetry or operational data.
- Do not claim that a tool was executed unless it actually was.
- Base technical conclusions on tool results.
- Distinguish observed facts from possible causes.
- If the available information is insufficient, say so.
- Never perform configuration changes or destructive operations.
"""

    user_prompt = f"""
User question:

{question}
"""

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(
                    text=f"{system_prompt}\n{user_prompt}"
                )
            ],
        )
    ]

    tool_config = types.GenerateContentConfig(
        tools=[
            types.Tool(
                function_declarations=TOOL_DECLARATIONS
            )
        ]
    )

    for round_number in range(MAX_TOOL_ROUNDS):

        logger.info(
            "Sending request to Gemini: round=%s",
            round_number + 1,
        )

        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=tool_config,
        )

        function_calls = response.function_calls

        if not function_calls:
            logger.info(
                "Gemini returned final response."
            )

            return response.text or (
                "Gemini returned an empty response."
            )

        # Preserve Gemini's original response content.
        #
        # This is important because Gemini's response can contain
        # function-call information that must remain in the
        # conversation history.
        contents.append(
            response.candidates[0].content
        )

        function_response_parts = []

        for function_call in function_calls:

            tool_name = function_call.name
            arguments = dict(function_call.args or {})

            logger.info(
                "Gemini requested tool=%s arguments=%s",
                tool_name,
                arguments,
            )

            result = execute_tool(
                tool_name=tool_name,
                arguments=arguments,
            )

            logger.info(
                "Tool result: tool=%s result=%s",
                tool_name,
                result,
            )

            function_response_parts.append(
                types.Part.from_function_response(
                    name=tool_name,
                    response={
                        "result": result,
                    },
                )
            )

        # Send all tool results back to Gemini.
        contents.append(
            types.Content(
                role="user",
                parts=function_response_parts,
            )
        )

    return (
        "The assistant reached the maximum number "
        "of tool execution rounds."
    )