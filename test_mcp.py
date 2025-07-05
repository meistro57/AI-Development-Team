#!/usr/bin/env python3
import asyncio
import json
import pytest
from mcp.client.session import ClientSession
from mcp.client.stdio import stdio_client

pytestmark = pytest.mark.asyncio


async def test_mcp_server():
    print("🧪 Testing AI Development Team MCP Server...")

    try:
        # Connect to our server
        async with stdio_client(["python", "ai_dev_team_server.py"]) as (read, write):
            async with ClientSession(read, write) as session:
                # Initialize
                await session.initialize()
                print("✅ Connected to AI Development Team!")

                # List available tools
                tools = await session.list_tools()
                print(f"\n🔧 Available tools ({len(tools.tools)}):")
                for tool in tools.tools:
                    print(f"  • {tool.name}: {tool.description}")

                # Test creating a project
                print("\n🚀 Testing project creation...")
                result = await session.call_tool(
                    "create_simple_project",
                    {
                        "name": "mcp-test-project",
                        "description": "Testing MCP integration with AI Development Team",
                    },
                )

                print("📋 Project creation result:")
                print(
                    json.dumps(
                        result.content[0].text if result.content else str(result),
                        indent=2,
                    )
                )

    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_mcp_server())
