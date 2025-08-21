# Libraries
from agents.mcp import MCPServerStdio

class MCPClient:
    """
        Class that implements an MCP client to connect to an MCP server.
    """
    def __init__(self):
        self.mcp_server:MCPServerStdio|None = None

    async def connect_to_server(self, server_script_path: str) -> MCPServerStdio:
        is_python = server_script_path.endswith(".py")

        if not is_python:
            raise ValueError("Server script must be a Python file.")
        
        self.mcp_server = MCPServerStdio(
            params={
                "command": "python",
                "args": [server_script_path],
            },
            cache_tools_list=True,
            name="mcp_client",
            client_session_timeout_seconds=30.0
        )
        await self.mcp_server.connect()
        return self.mcp_server

    async def cleanup(self):
        await self.mcp_server.cleanup()

