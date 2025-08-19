from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

from constants import SERVER_URL, USER_AGENT

# Initialize FastMCP server
mcp = FastMCP("management_server")

async def make_management_server_request(endpoint: str) -> Any:
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(endpoint, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

# MCP tools for user management
@mcp.tool("get_users")
async def get_users() -> Any:
    """
        Retrieve a list of users from the management server.
    """
    url = f"{SERVER_URL}/users/"
    return await make_management_server_request(url)

@mcp.tool("create_user")
async def create_user(user_name: str) -> Any:
    """
        Create a new user on the management server.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    data = {"user_name": user_name}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SERVER_URL}/users/", json=data, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

@mcp.tool("delete_user")
async def delete_user(user_id: str) -> Any:
    """
        Create a new user on the management server.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    

    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{SERVER_URL}/users/" + user_id, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

    url = f"{SERVER_URL}/users/"
    return await make_management_server_request(url)

@mcp.tool("update_user")
async def update_user(user_id: str, user_name: str) -> Any:
    """
        Update an existing user on the management server.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    data = {"user_name": user_name}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{SERVER_URL}/users/" + user_id, json=data, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None


# MCP tools for user - privilege 
@mcp.tool("get_privileges_of_user")
async def get_privileges_of_user(user_id: str) -> Any:
    """
        Retrieve a list of privileges for a specific user.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVER_URL}/user_privileges/" + user_id, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

@mcp.tool("add_privileges_to_user")
async def add_privileges_to_user(user_id: str, arr_id_privileges: list[str]) -> Any:
    """
        Add privileges to a user.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    
    data = {"arr_id_privileges": arr_id_privileges}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{SERVER_URL}/grant_privileges/" + user_id, json=data, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None
        
@mcp.tool("delete_privileges_to_user")
async def delete_privileges_to_user(user_id: str, arr_id_privileges: list[str]) -> Any:
    """
        Delete privileges from a user.
    """
    
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    
    data = {"arr_id_privileges": arr_id_privileges}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{SERVER_URL}/revoke_privileges/" + user_id, json=data, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

@mcp.tool("get_all_privileges")
async def get_all_privileges() -> Any:
    """
        Retrieve all privileges.
    """
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{SERVER_URL}/privileges/", headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return None

if __name__ == "__main__":
    print("Starting MCP Management Server...")
    server = mcp.run(transport="stdio")

