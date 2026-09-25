import logging
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


load_dotenv()

logger = logging.getLogger(__name__)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

MCP_SERVER_PATH = (
    PROJECT_ROOT
    / "src"
    / "enterprise_network_ai"
    / "mcp_server.py"
)

MAX_TOOL_ROUNDS = 5


def get_gemini_client() -> genai.Client:
    """
    Create a Gemini API client.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY environment variable "
            "is not configured."
        )

    return genai.Client(
        api_key=api_key,
    )


def get_mcp_server_parameters() -> StdioServerParameters:
    """
    Build configuration for starting the local
    FastMCP server through stdio.
    """

    return StdioServerParameters(
        command="uv",
        args=[
            "run",
            "python",
            str(MCP_SERVER_PATH),
        ],
        cwd=str(PROJECT_ROOT),
    )


def sanitize_schema(
    schema: dict[str, Any],
) -> dict[str, Any]:
    """
    Convert an MCP JSON schema into a schema that
    can safely be passed to Gemini function calling.

    FastMCP can generate:
        "additionalProperties": false

    Some google-genai MCP conversion paths currently
    incorrectly treat that boolean as a dictionary.
    We therefore remove that field from the schema
    before passing the declaration to Gemini.
    """

    result: dict[str, Any] = {}

    for key, value in schema.items():

        if key in {
            "additionalProperties",
            "additional_properties",
        }:
            continue

        if key == "properties" and isinstance(value, dict):

            result[key] = {
                property_name: sanitize_schema(
                    property_schema
                )
                if isinstance(property_schema, dict)
                else property_schema
                for property_name, property_schema
                in value.items()
            }

        elif key in {
            "items",
            "additionalItems",
        } and isinstance(value, dict):

            result[key] = sanitize_schema(value)

        elif key in {
            "anyOf",
            "oneOf",
            "allOf",
        } and isinstance(value, list):

            result[key] = [
                sanitize_schema(item)
                if isinstance(item, dict)
                else item
                for item in value
            ]

        elif key in {
            "$defs",
            "defs",
        } and isinstance(value, dict):

            result[key] = {
                definition_name: sanitize_schema(
                    definition_schema
                )
                if isinstance(definition_schema, dict)
                else definition_schema
                for definition_name, definition_schema
                in value.items()
            }

        else:
            result[key] = value

    return result


def build_gemini_tools(
    mcp_tools: list[Any],
) -> list[types.Tool]:
    """
    Convert MCP tool definitions into Gemini
    function declarations.

    We intentionally perform this conversion ourselves
    instead of using google-genai's built-in MCP adapter.
    """

    function_declarations = []

    for mcp_tool in mcp_tools:

        input_schema = getattr(
            mcp_tool,
            "inputSchema",
            getattr(
                mcp_tool,
                "input_schema",
                {},
            ),
        )

        clean_schema = sanitize_schema(
            input_schema
        )

        declaration = types.FunctionDeclaration(
            name=mcp_tool.name,
            description=mcp_tool.description or "",
            parameters_json_schema=clean_schema,
        )

        function_declarations.append(
            declaration
        )

        logger.info(
            "Converted MCP tool: %s",
            mcp_tool.name,
        )

    return [
        types.Tool(
            function_declarations=function_declarations
        )
    ]


def extract_mcp_result(
    tool_result: Any,
) -> Any:
    """
    Convert an MCP CallToolResult into a JSON-like
    value suitable for Gemini.
    """

    structured_content = getattr(
        tool_result,
        "structuredContent",
        None,
    )

    if structured_content is None:

        structured_content = getattr(
            tool_result,
            "structured_content",
            None,
        )

    if structured_content is not None:
        return structured_content

    data = getattr(
        tool_result,
        "data",
        None,
    )

    if data is not None:
        return data

    content = getattr(
        tool_result,
        "content",
        None,
    )

    if content is not None:

        result = []

        for item in content:

            text = getattr(
                item,
                "text",
                None,
            )

            if text is not None:
                result.append(text)

        if result:
            return result

    return str(tool_result)


async def execute_mcp_tool(
    session: ClientSession,
    tool_name: str,
    arguments: dict[str, Any],
) -> dict[str, Any]:
    """
    Execute a tool through the MCP client.
    """

    logger.info(
        "Calling MCP tool=%s arguments=%s",
        tool_name,
        arguments,
    )

    try:

        result = await session.call_tool(
            tool_name,
            arguments,
        )

        data = extract_mcp_result(result)

        return {
            "success": True,
            "data": data,
        }

    except Exception as exc:

        logger.exception(
            "MCP tool failed: %s",
            tool_name,
        )

        return {
            "success": False,
            "error": str(exc),
        }


async def ask_network_assistant(
    question: str,
) -> str:
    """
    Use Gemini for reasoning and MCP for network
    tool discovery and execution.
    """

    model = os.getenv(
        "GEMINI_MODEL",
        "gemini-3.7-flash",
    )

    gemini_client = get_gemini_client()

    server_params = get_mcp_server_parameters()

    prompt = f"""
You are an enterprise network troubleshooting assistant.

You have access to read-only network diagnostic tools.

Rules:
- Use tools when live network information is required.
- Never invent telemetry.
- Base conclusions on tool results.
- Distinguish observed facts from possible causes.
- If information is insufficient, say so.
- Never perform configuration changes.

User question:

{question}
"""

    async with stdio_client(
        server_params
    ) as (read, write):

        async with ClientSession(
            read,
            write,
        ) as session:

            logger.info(
                "Initializing MCP session."
            )

            await session.initialize()

            # -------------------------------------------------
            # 1. Discover tools from MCP
            # -------------------------------------------------

            tools_result = await session.list_tools()

            mcp_tools = tools_result.tools

            logger.info(
                "Discovered MCP tools: %s",
                [
                    tool.name
                    for tool in mcp_tools
                ],
            )

            # -------------------------------------------------
            # 2. Convert MCP schemas into Gemini declarations
            # -------------------------------------------------

            gemini_tools = build_gemini_tools(
                mcp_tools
            )

            # -------------------------------------------------
            # 3. Build conversation
            # -------------------------------------------------

            contents = [
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(
                            text=prompt
                        )
                    ],
                )
            ]

            # -------------------------------------------------
            # 4. Agent/tool loop
            # -------------------------------------------------

            for round_number in range(
                MAX_TOOL_ROUNDS
            ):

                logger.info(
                    "Gemini request round=%s",
                    round_number + 1,
                )

                response = (
                    await gemini_client.aio.models.generate_content(
                        model=model,
                        contents=contents,
                        config=types.GenerateContentConfig(
                            temperature=0,
                            tools=gemini_tools,
                        ),
                    )
                )

                function_calls = (
                    response.function_calls
                )

                # -------------------------------------------------
                # No function calls = final answer
                # -------------------------------------------------

                if not function_calls:

                    logger.info(
                        "Gemini returned final response."
                    )

                    return response.text or (
                        "Gemini returned an empty response."
                    )

                # -------------------------------------------------
                # Preserve Gemini's function-call response
                # -------------------------------------------------

                contents.append(
                    response.candidates[0].content
                )

                # -------------------------------------------------
                # Execute requested MCP tools
                # -------------------------------------------------

                function_response_parts = []

                for function_call in function_calls:

                    tool_name = (
                        function_call.name
                    )

                    arguments = dict(
                        function_call.args or {}
                    )

                    logger.info(
                        "Gemini requested tool=%s arguments=%s",
                        tool_name,
                        arguments,
                    )

                    tool_result = (
                        await execute_mcp_tool(
                            session=session,
                            tool_name=tool_name,
                            arguments=arguments,
                        )
                    )

                    logger.info(
                        "MCP result tool=%s result=%s",
                        tool_name,
                        tool_result,
                    )

                    function_response_parts.append(
                        types.Part.from_function_response(
                            name=tool_name,
                            response={
                                "result": tool_result,
                            },
                        )
                    )

                # -------------------------------------------------
                # Send tool results back to Gemini
                # -------------------------------------------------

                contents.append(
                    types.Content(
                        role="user",
                        parts=function_response_parts,
                    )
                )

            return (
                "The assistant reached the maximum "
                "number of tool execution rounds."
            )