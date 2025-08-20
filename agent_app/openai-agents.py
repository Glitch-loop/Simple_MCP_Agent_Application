# openai-agents
from agents import Agent, Runner, GuardrailFunctionOutput, InputGuardrail
from agents.exceptions import InputGuardrailTripwireTriggered
from agents.run_context import RunContextWrapper
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.server.fastmcp import FastMCP
from typing import Optional
from contextlib import AsyncExitStack
from agents.mcp import MCPServerStdio

# Libraries
import asyncio
import os
from dotenv import load_dotenv
import openai
from pydantic import BaseModel

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class MCPClient:
    def __init__(self):
        self.session: Optional[ClientSession] = None
        self.exist_stack: AsyncExitStack = AsyncExitStack()
        self.mcp = FastMCP("mcp_client")
        self.mcp_server:MCPServerStdio|None = None

    async def connect_to_server(self, server_script_path: str):
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
        print(f"Connecting to MCP server at {self.mcp_server}...")
        return self.mcp_server

    async def cleanup(self):
        await self.exist_stack.aclose()


# Interface for guardrail function output
class HomeworkOutput(BaseModel):
    is_homework: bool
    reasoning: str

# Define the agents with their specific instructions and handoff descriptions
history_tutor_agent = Agent(
    name="History Tutor",
    handoff_description="Specialist agent for historical questions",
    instructions="You provide assistance with historical queries. Explain important events and context clearly.",
)

math_tutor_agent = Agent(
    name="Math Tutor",
    handoff_description="Specialist agent for math questions",
    instructions="You provide help with math problems. Explain your reasoning at each step and include examples",
)

# Guardrail agent that checks if the user is asking about homework
guardrail_agent = Agent(
    name="Guardrail check",
    instructions="Check if the user is asking about homework.",
    output_type=HomeworkOutput,
)

async def homework_guardrail(ctx, agent, input_data):
    result = await Runner.run(guardrail_agent, input_data, context=ctx.context)
    final_output = result.final_output_as(HomeworkOutput)
    return GuardrailFunctionOutput(
        output_info=final_output,
        tripwire_triggered=not final_output.is_homework,
    )


async def main():
    # Example 1: History question
    # try:
    #     result = await Runner.run(triage_agent, "who was the first president of the united states?")
    #     print(result.final_output)
    # except InputGuardrailTripwireTriggered as e:
    #     print("Guardrail blocked this input:", e)

    # Example 2: General/philosophical question
    # try:
    #     result = await Runner.run(triage_agent, "What is the meaning of life?")
    #     print(result.final_output)
    # except InputGuardrailTripwireTriggered as e:
    #     print("Guardrail blocked this input:", e)

    # Triage agent that decides which specialist agent to use based on the user's question
    client = MCPClient()
    mcp_server = await client.connect_to_server("D:/DOCUMENTS/self_study/Agents/mcp_server/selling_server/mcp_selling_server.py")
    

    print("mcp_server:", mcp_server)
    triage_agent = Agent(
        name="Triage Agent",
        instructions="You determine which agent to use based on the user's homework question",
        handoffs=[history_tutor_agent, math_tutor_agent],
        mcp_servers=[mcp_server],
        
        # input_guardrails=[InputGuardrail(guardrail_function=homework_guardrail)]
    )

    while True:
        try:
            query = input("\n\nQuery: ").strip()

            if query.lower() == "quit":
                break
            
            result = await Runner.run(triage_agent, query)
            print(result)
            print("\n" + result.final_output)

        except Exception as e:
            print(f"Error: {str(e)}")
    
    await client.cleanup()

        

asyncio.run(main())
