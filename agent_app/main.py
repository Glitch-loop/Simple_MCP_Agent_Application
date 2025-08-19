import asyncio
from agent_app.mcp_client import MCPClient

async def main():
    if len(sys.argv) < 2:
        print(sys.argv)
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.connect_to_server(sys.argv[2])
        await client.chat_tool()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())