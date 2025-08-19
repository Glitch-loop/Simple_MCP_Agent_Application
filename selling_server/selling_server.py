import os
from supabase import create_client, Client
from fastapi import FastAPI, Body
from selling_server.interfaces import CreateClientRequest, UpdateClientRequest, CreateProductRequest, UpdateProductRequest, CreateSellingRequest, UpdateSellingRequest

app = FastAPI()

def create_connection() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    return supabase

# CRUD for Client
@app.post("/clients/")
def create_client_entry(request: CreateClientRequest = Body(...)):
    supabase = create_connection()
    response = supabase.table("Client").insert({"client_name": request.client_name, "email": request.email}).execute()
    return response.data

@app.get("/clients/")
def list_clients():
    supabase = create_connection()
    response = supabase.table("Client").select("*").execute()
    return response.data

@app.get("/clients/{client_id}")
def get_client(client_id: str):
    supabase = create_connection()
    response = supabase.table("Client").select("*").eq("id_client", client_id).single().execute()
    return response.data

@app.put("/clients/{client_id}")
def update_client(client_id: str, request: UpdateClientRequest = Body(...)):
    supabase = create_connection()
    data = {}
    if request.client_name is not None:
        data["client_name"] = request.client_name
    if request.email is not None:
        data["email"] = request.email
    response = supabase.table("Client").update(data).eq("id_client", client_id).execute()
    return response.data

@app.delete("/clients/{client_id}")
def delete_client(client_id: str):
    supabase = create_connection()
    response = supabase.table("Client").delete().eq("id_client", client_id).execute()
    return {"deleted": response.data}

# CRUD for Product
@app.post("/products/")
def create_product(request: CreateProductRequest = Body(...)):
    supabase = create_connection()
    response = supabase.table("Product").insert({"product_name": request.product_name, "price": request.price}).execute()
    return response.data

@app.get("/products/")
def list_products():
    supabase = create_connection()
    response = supabase.table("Product").select("*").execute()
    return response.data

@app.get("/products/{product_id}")
def get_product(product_id: str):
    supabase = create_connection()
    response = supabase.table("Product").select("*").eq("id_product", product_id).single().execute()
    return response.data

@app.put("/products/{product_id}")
def update_product(product_id: str, request: UpdateProductRequest = Body(...)):
    supabase = create_connection()
    data = {}
    if request.product_name is not None:
        data["product_name"] = request.product_name
    if request.price is not None:
        data["price"] = request.price
    response = supabase.table("Product").update(data).eq("id_product", product_id).execute()
    return response.data

@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    supabase = create_connection()
    response = supabase.table("Product").delete().eq("id_product", product_id).execute()
    return {"deleted": response.data}

# CRUD for Selling
@app.post("/sellings/")
def create_selling(request: CreateSellingRequest = Body(...)):
    supabase = create_connection()
    response = supabase.table("Sellings").insert({
        "id_client": request.id_client,
        "id_product": request.id_product,
        "price_at_moment": request.price_at_moment
    }).execute()
    return response.data

@app.get("/sellings/")
def list_sellings():
    supabase = create_connection()
    response = supabase.table("Sellings").select("*").execute()
    return response.data

@app.get("/sellings/{selling_id}")
def get_selling(selling_id: str):
    supabase = create_connection()
    response = supabase.table("Sellings").select("*").eq("id", selling_id).single().execute()
    return response.data

@app.put("/sellings/{selling_id}")
def update_selling(selling_id: str, request: UpdateSellingRequest = Body(...)):
    supabase = create_connection()
    data = {}
    if request.id_client is not None:
        data["id_client"] = request.id_client
    if request.id_product is not None:
        data["id_product"] = request.id_product
    if request.price_at_moment is not None:
        data["price_at_moment"] = request.price_at_moment
    response = supabase.table("Sellings").update(data).eq("id", selling_id).execute()
    return response.data

@app.delete("/sellings/{selling_id}")
def delete_selling(selling_id: str):
    supabase = create_connection()
    response = supabase.table("Sellings").delete().eq("id", selling_id).execute()
    return {"deleted": response.data}
