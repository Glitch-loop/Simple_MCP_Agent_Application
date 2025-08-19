import os
from supabase import create_client, Client
from fastapi import FastAPI

from dotenv import load_dotenv

from management_server.interfaces import (
    create_user_request,
    update_user_request,
    privilege_request
)

app = FastAPI()
load_dotenv()

def create_connection() -> Client:
    url: str = os.environ.get("SUPABASE_URL")
    key: str = os.environ.get("SUPABASE_KEY")
    supabase: Client = create_client(url, key)
    
    return supabase


@app.post("/users/")
def create_user(request: create_user_request):
    supabase = create_connection()
    response = supabase.table("Users").insert({"user_name": request.user_name}).execute()
    return response.data

@app.get("/users/")
def list_users():
    supabase = create_connection()
    response = supabase.table("Users").select("*").execute()
    return response.data

@app.get("/users/{user_id}")
def get_user(user_id: str):
    supabase = create_connection()
    response = supabase.table("Users").select("*").eq("id_user", user_id).single().execute()
    return response.data

@app.put("/users/{user_id}")
def update_user(user_id: str, request: update_user_request):
    print("Updating user:", user_id, "with new name:", request.user_name)
    supabase = create_connection()
    response = supabase.table("Users").update({"user_name": request.user_name}).eq("id_user", user_id).execute()
    print("Update response:", response)
    return response.data

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    supabase = create_connection()
    response = supabase.table("Users").delete().eq("id_user", user_id).execute()
    return {"deleted": response.data}

# Privileges CRUD
@app.post("/privileges/")
def create_privilege(privilege_name: str, privilege_description: str = None):
    supabase = create_connection()
    data = {"privilege_name": privilege_name}
    if privilege_description:
        data["privilege_description"] = privilege_description
    response = supabase.table("Privileges").insert(data).execute()
    return response.data

@app.get("/privileges/")
def list_privileges():
    supabase = create_connection()
    response = supabase.table("Privileges").select("*").execute()
    return response.data

@app.get("/privileges/{privilege_id}")
def get_privilege(privilege_id: str):
    supabase = create_connection()
    response = supabase.table("Privileges").select("*").eq("id_privilege", privilege_id).single().execute()
    return response.data

@app.put("/privileges/{privilege_id}")
def update_privilege(privilege_id: str, privilege_name: str = None, privilege_description: str = None):
    supabase = create_connection()
    data = {}
    if privilege_name:
        data["privilege_name"] = privilege_name
    if privilege_description:
        data["privilege_description"] = privilege_description
    response = supabase.table("Privileges").update(data).eq("id_privilege", privilege_id).execute()
    return response.data

@app.delete("/privileges/{privilege_id}")
def delete_privilege(privilege_id: str):
    supabase = create_connection()
    response = supabase.table("Privileges").delete().eq("id_privilege", privilege_id).execute()
    return {"deleted": response.data}

@app.post("/grant_privileges/{id_user}")
def grant_privileges(id_user: str, request: privilege_request):
    supabase = create_connection()
    data = [
        {"id_user": id_user, "id_privilege": privilege_id}
        for privilege_id in request.arr_id_privileges
    ]
    response = supabase.table("Users_X_Privileges").insert(data).execute()
    return {"granted": response.data}

@app.post("/revoke_privileges/{id_user}")
def revoke_privileges(id_user: str, request: privilege_request):
    supabase = create_connection()
    deleted = []
    for privilege_id in request.arr_id_privileges:
        resp = supabase.table("Users_X_Privileges").delete().eq("id_user", id_user).eq("id_privilege", privilege_id).execute()
        deleted.append(resp.data)
    return {"revoked": deleted}

@app.get("/user_privileges/{id_user}")
def user_privileges(id_user: str):
    supabase = create_connection()
    response = supabase.table("Users_X_Privileges").select("id_privilege").eq("id_user", id_user).execute()
    privilege_ids = [row["id_privilege"] for row in response.data]
    if not privilege_ids:
        return {"privileges": []}
    privileges = supabase.table("Privileges").select("*").in_("id_privilege", privilege_ids).execute()
    return {"privileges": privileges.data}