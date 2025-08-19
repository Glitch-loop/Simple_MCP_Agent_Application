from pydantic import BaseModel, Field
from typing import List

class create_user_request(BaseModel):
    user_name: str = Field(description="Name of the user to be created")

class update_user_request(BaseModel):
    user_name: str = Field(description="New name of the user")


class privilege_request(BaseModel):
    arr_id_privileges: List[str] = Field(description="List of privilege IDs to be added to the user")
