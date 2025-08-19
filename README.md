# Simple MCP agent application
This project was created to put hands-on in the development of AI applications.

With this project I try to put in practice two concepts:
- Create MCP servers
- Create specialized agents that interacts one each other resulting in the desired behavior.

## What is the project about?
Just for giving a context I decided to create a simple store system.

To keep the things simple, the system was divided into two main areas:
- *sellings:* All related to selling and products
- *system_management:* Users and privileges.


## Structure of the project
The project is composed of three main modules:
- agent_app: Host and MCP client server. Application 
- management_server: MCP server
- selling_server: MCP server

## Experiments
Just for experimenting

Validation through the model.

It was insteresting for me to use a model for validating who are you and then 

# Commands
## Run servers
Command to run the application

Note: Notice that we pass the path to the mcp server through the command

```
    uv run .\agent_app\mcp_client.py D:\DOCUMENTS\self_study\Agents\mcp_server\management_server\mcp_management_server.py D:\DOCUMENTS\self_study\Agents\mcp_server\selling_server\mcp_selling_server.py

```

## Run web servers
Command to run the webservers

**Management server**
```
    uvicorn management_server.management_server:app --reload --port 8000
```

**Selling server**
```
    uvicorn selling_server.selling_server:app --reload --port 8001
```
