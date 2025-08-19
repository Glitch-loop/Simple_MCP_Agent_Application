import asyncio
from typing import Optional
from contextlib import AsyncExitStack
import httpx
from mcp.server.fastmcp import FastMCP

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from openai import OpenAI
from dotenv import load_dotenv
import os
import json

load_dotenv()

context_window = []

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exist_stack: AsyncExitStack = AsyncExitStack()
        self.openai = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_API_BASE_URL", "https://api.openai.com/v1")
        )
        self.mcp = FastMCP("mcp_client")

    async def connect_to_server(self, server_script_path: str):
        """
        Connect to the MCP server using the provided script path.
        """
        is_python = server_script_path.endswith(".py")
        is_js = server_script_path.endswith(".js")

        if not (is_python or is_js):
            raise ValueError("Server script must be a Python or JavaScript file.")

        command = "python" if is_python else "node"

        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exist_stack.enter_async_context(
            stdio_client(server_params)
        )
        self.stidio, self.write = stdio_transport
        self.session = await self.exist_stack.enter_async_context(
            ClientSession(self.stidio, self.write)
        )

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("Connected to server with tools:", [tool.name for tool in tools])
    
    async def process_query(self, query: str) -> str:
        """
        Process a query using the MCP server and return the response.
        """

        messages = []

        if len(context_window) > 0:
            # Use existing context window if available
            context_window.append({
                "role": "user",
                "content": query
            })
        
        else:
            # Initialize context window with developer instructions
            context_window.append({
                    "role": "developer",
                    "content": "If the user wants to make an operation related to user management, you have to authenticate the user first asking who he is, and then once you already know who is, then verify if the user has the privileges to perform the operation. Beaware that if the user has some privilege of user management, implicity, he could list or retrieve information from the system."
            })
            context_window.append({
                    "role": "user",
                    "content": query
            })
        
        messages = context_window.copy()


        # Get available tools
        response = await self.session.list_tools()
        available_tools = [
            {   
                "type": "function",
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            } for tool in response.tools
        ]

        final_text = []
        assistant_message_content = []
        thought_process = True

        while thought_process:
            messages.extend(assistant_message_content)

            response = self.openai.responses.create(
                model="gpt-4.1",
                input=messages,
                tools=available_tools,
            )
        
            for output in response.output:
                if output.type == "message":
                    model_answer = output.content[0]
                    final_text.append(model_answer.text)
                    assistant_message_content.append({
                        "role": "assistant",
                        "content": model_answer.text
                    })
                    
                elif output.type == "function_call":
                    # Extract tool call details
                    tool_name = output.name
                    tool_args = json.loads(output.arguments)
                    tool_call_id = output.call_id
                    
                    print("\033[92mCalling tool:", tool_name)

                    assistant_message_content.append({
                        "call_id": tool_call_id,
                        "type": "function_call",
                        "name": tool_name,
                        "arguments": json.dumps(tool_args)
                    })


                    # Execute tool call
                    result = await self.session.call_tool(tool_name, tool_args)
                    
                    result_call_function = []

                    for item in result.content:
                        result_call_function.append(json.loads(item.text))                                
                    
                    # Append tool call 
                    assistant_message_content.append({
                        "type": "function_call_output",
                        "call_id": tool_call_id,
                        "output": json.dumps(result_call_function)
                    })

            thought_process = self.has_call_tool(response)

        context_window.append({
                "role": "assistant",
                "content": "".join(final_text)
        })
        
        return "\n".join(final_text)

    def has_call_tool(self, response) -> bool:
        """
        Check if the output contains a tool call.
        """
        return any(
            output.type == "function_call" for output in response.output
        )


    async def chat_tool(self):
        "Run an interactive chat loop"
        
        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == "quit":
                    break
                if query.lower() == "reset":
                    context_window.clear()
                    print("\033[0mcontext window cleaned")
                    continue

                response = await self.process_query(query)
                print("\n" + response)
            except Exception as e:
                print(f"Error: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exist_stack.aclose()

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