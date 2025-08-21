from agents import Agent, Runner
import os
from dotenv import load_dotenv
import openai

from mcp_client import MCPClient
from conversation_state import ConversationState  
from interfaces.interfaces import text_message

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

class MCPHost:
    """
        Class that implements an MCP host. 
        This class contains the business logic to interact with the agents and the MCP server (AI application). 
    """
    def __init__(self):
        # Creating MCP clients
        self.mcp_client_system_management:MCPClient = MCPClient()
        self.mcp_client_selling_server:MCPClient = MCPClient()

        # Creating agents
        self.system_manager_agent:Agent|None = None
        self.selling_server_agent:Agent|None = None
        self.orchestrator_agent:Agent|None = None

        # Conversation state
        # self.conversation_state:ConversationState = ConversationState()

    async def connect_with_servers(self):
        # Creating connection to MCP servers
        
        print("Connecting servers...")
        print("management server: ", await self.mcp_client_system_management.connect_to_server(os.getenv("MCP_SYSTEM_MANAGEMENT_SERVER_PATH")))
        print("selling server: ", await self.mcp_client_selling_server.connect_to_server(os.getenv("MCP_SELLING_SERVER_PATH")))

    async def create_agents(self):
        # Creating agents
        print("Creating agents...")
        self.system_manager_agent = Agent(
            name="System Manager Agent",
            model="gpt-4.1",
            handoff_description="Specialist agent for system management tasks",
            instructions="You are responsible for managing system configurations and settings. Depending on what the user ask you, you will choose between your tools the appropoate one for answering the query.",
            mcp_servers=[self.mcp_client_system_management.mcp_server]
        )
        self.selling_server_agent = Agent(
            name="Selling Server Agent",
            model="gpt-4.1",
            handoff_description="Specialist agent for selling server tasks",
            instructions="You handle all operations related to the selling server, including managing clients, products, and sales records. Depending on what the user ask you, you will choose between your tools the appropoate one for answering the query.",
            mcp_servers=[self.mcp_client_selling_server.mcp_server]
        )

        orchestrator_prompt = """
            #############################
            SECURITY

            You are responsible for authenticating the user before performing any actions. Always follow these steps:

            User Identification:
            Prompt the user to identify themselves. If the user has already been authenticated in the current conversation state, proceed to the next step. If not, check the database to verify the user's existence.

            Privilege Verification:
            After identifying the user, check their privileges to determine if they are authorized to perform the requested operation. Note that privileges for actions like delete, update, or insert also implicitly grant permission to retrieve or list data (e.g., if a user can delete, they can also get or list clients).

            Action Execution:
            Only after successful authentication and privilege verification should you proceed to perform the requested action.

            #######################################################

            Context
            You are the orchestrator agent. Your role is to determine which specialist agent (System Manager or Selling Server) 
            is best suited to handle the user's request. 
            
            Analyze the request carefully and delegate it to the appropriate agent. 
            If the request involves system configurations, delegate it to the System Manager Agent. If it involves client, product, 
            or sales management, delegate it to the Selling Server Agent. Ensure smooth communication and task handoff between agents. 
            
            #############################
            SECURITY

            You are responsible for authenticating the user before performing any actions. Always follow these steps:

            User Identification:
            Prompt the user to identify themselves. If the user has already been authenticated in the current conversation state, proceed to the next step. If not, check the database to verify the user's existence.

            Privilege Verification:
            After identifying the user, check their privileges to determine if they are authorized to perform the requested operation. Note that privileges for actions like delete, update, or insert also implicitly grant permission to retrieve or list data (e.g., if a user can delete, they can also get or list clients).

            Action Execution:
            Only after successful authentication and privilege verification should you proceed to perform the requested action.

        """
        self.orchestrator_agent = Agent(
            name="Orchestrator Agent",
            model="gpt-4.1",
            handoff_description="Agent that orchestrates tasks between the System Manager and Selling Server agents",
            instructions=orchestrator_prompt,
            handoffs=[self.system_manager_agent, self.selling_server_agent]
        )

    async def chat_with_agent(self) -> None:
        """
        Method to chat with the orchestrator agent and get a response.
        :param query: The user's query to be processed by the agent.
        :return: The response from the agent.
        """

        if (self.orchestrator_agent is not None
        and self.selling_server_agent is None
        and self.system_manager_agent):
            return  

        conversation_state:ConversationState = ConversationState() 

        while True:
            try:
                query = input("\n\nQuery: ").strip()

                if query.lower() == "quit":
                    break
                if query.lower() == "reset":
                    conversation_state.clear_history()
                    print("Conversation history cleared.")
                    continue
                
                conversation_state.add_message("user", query)
                
                result = await Runner.run(self.orchestrator_agent, conversation_state.get_history())

                print("\n" + result.final_output)

                conversation_state.update_history(result.to_input_list())

            except Exception as e:
                print(f"Error: {str(e)}")
        
        await self.mcp_client_system_management.cleanup()
        await self.mcp_client_selling_server.cleanup()
        print("Chat session ended.")
        
        return 
    