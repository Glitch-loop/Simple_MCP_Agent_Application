from pydantic import BaseModel

class text_message(BaseModel):
    role: str
    content: str
