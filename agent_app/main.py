import asyncio

# from agent_app.vanilla_mcp_client import MCPClient
from mcp_host import MCPHost

async def main():
    # if len(sys.argv) < 2:
    #     print(sys.argv)
    #     print("Usage: python client.py <path_to_server_script>")
    #     sys.exit(1)

    # client = MCPClient()
    # try:
    #     await client.connect_to_server(sys.argv[1])
    #     await client.connect_to_server(sys.argv[2])
    #     await client.chat_tool()
    # finally:
    #     await client.cleanup()
    print("Starting MCP Host...")
    host_app = MCPHost()

    await host_app.connect_with_servers()
    await host_app.create_agents()

    await host_app.chat_with_agent()

if __name__ == "__main__":
    
    asyncio.run(main())