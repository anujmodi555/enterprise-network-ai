import asyncio
from pathlib import Path

from fastmcp import Client


MCP_SERVER_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "enterprise_network_ai"
    / "mcp_server.py"
)


async def main() -> None:

    print("MCP server:")
    print(MCP_SERVER_PATH)

    async with Client(MCP_SERVER_PATH) as client:

        print("\n=== AVAILABLE TOOLS ===")

        tools = await client.list_tools()

        for tool in tools:
            print(f"\nName: {tool.name}")
            print(f"Description: {tool.description}")
            print(f"Input schema: {tool.input_schema}")

        print("\n=== CALLING TOOL ===")

        result = await client.call_tool(
            "get_device_status",
            {
                "device_id": "R1",
            },
        )

        print("\nTool result:")
        print(result)

        print("\nStructured data:")
        print(result.data)


if __name__ == "__main__":
    asyncio.run(main())