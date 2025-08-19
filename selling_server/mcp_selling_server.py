from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

SELLING_SERVER_URL = "http://localhost:8001"  # Change port if needed
USER_AGENT = "Selling-server/1.0"

mcp = FastMCP("selling_server")

def get_headers():
    return {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }

async def make_request(method: str, endpoint: str, data: Any = None) -> Any:
    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(endpoint, headers=get_headers(), timeout=30.0)
            elif method == "POST":
                response = await client.post(endpoint, json=data, headers=get_headers(), timeout=30.0)
            elif method == "PUT":
                response = await client.put(endpoint, json=data, headers=get_headers(), timeout=30.0)
            elif method == "DELETE":
                response = await client.delete(endpoint, headers=get_headers(), timeout=30.0)
            else:
                return None
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

# CLIENTS
@mcp.tool("list_clients")
async def list_clients() -> Any:
    return await make_request("GET", f"{SELLING_SERVER_URL}/clients/")

@mcp.tool("get_client")
async def get_client(client_id: str) -> Any:
    return await make_request("GET", f"{SELLING_SERVER_URL}/clients/{client_id}")

@mcp.tool("create_client")
async def create_client(client_name: str, email: str) -> Any:
    data = {"client_name": client_name, "email": email}
    return await make_request("POST", f"{SELLING_SERVER_URL}/clients/", data)

@mcp.tool("update_client")
async def update_client(client_id: str, client_name: str = None, email: str = None) -> Any:
    data = {k: v for k, v in {"client_name": client_name, "email": email}.items() if v is not None}
    return await make_request("PUT", f"{SELLING_SERVER_URL}/clients/{client_id}", data)

@mcp.tool("delete_client")
async def delete_client(client_id: str) -> Any:
    return await make_request("DELETE", f"{SELLING_SERVER_URL}/clients/{client_id}")

# PRODUCTS
@mcp.tool("list_products")
async def list_products() -> Any:
    return await make_request("GET", f"{SELLING_SERVER_URL}/products/")

@mcp.tool("get_product")
async def get_product(product_id: str) -> Any:
    return await make_request("GET", f"{SELLING_SERVER_URL}/products/{product_id}")

@mcp.tool("create_product")
async def create_product(product_name: str, price: float) -> Any:
    data = {"product_name": product_name, "price": price}
    return await make_request("POST", f"{SELLING_SERVER_URL}/products/", data)

@mcp.tool("update_product")
async def update_product(product_id: str, product_name: str = None, price: float = None) -> Any:
    data = {k: v for k, v in {"product_name": product_name, "price": price}.items() if v is not None}
    return await make_request("PUT", f"{SELLING_SERVER_URL}/products/{product_id}", data)

@mcp.tool("delete_product")
async def delete_product(product_id: str) -> Any:
    return await make_request("DELETE", f"{SELLING_SERVER_URL}/products/{product_id}")

# SELLINGS
@mcp.tool("list_sellings")
async def list_sellings() -> Any:
    return await make_request("GET", f"{SELLING_SERVER_URL}/sellings/")

@mcp.tool("get_selling")
async def get_selling(selling_id: str) -> Any:
    return await make_request("GET", f"{SELLING_SERVER_URL}/sellings/{selling_id}")

@mcp.tool("create_selling")
async def create_selling(id_client: str, id_product: str, price_at_moment: float) -> Any:
    data = {"id_client": id_client, "id_product": id_product, "price_at_moment": price_at_moment}
    return await make_request("POST", f"{SELLING_SERVER_URL}/sellings/", data)

@mcp.tool("update_selling")
async def update_selling(selling_id: str, id_client: str = None, id_product: str = None, price_at_moment: float = None) -> Any:
    data = {k: v for k, v in {"id_client": id_client, "id_product": id_product, "price_at_moment": price_at_moment}.items() if v is not None}
    return await make_request("PUT", f"{SELLING_SERVER_URL}/sellings/{selling_id}", data)

@mcp.tool("delete_selling")
async def delete_selling(selling_id: str) -> Any:
    return await make_request("DELETE", f"{SELLING_SERVER_URL}/sellings/{selling_id}")

if __name__ == "__main__":
    print("Starting MCP Selling Server...")
    server = mcp.run(transport="stdio")
