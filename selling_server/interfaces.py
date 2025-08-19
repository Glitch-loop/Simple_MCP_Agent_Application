from pydantic import BaseModel, EmailStr
from typing import Optional

class CreateClientRequest(BaseModel):
    client_name: str
    email: EmailStr

class UpdateClientRequest(BaseModel):
    client_name: Optional[str] = None
    email: Optional[EmailStr] = None

class CreateProductRequest(BaseModel):
    product_name: str
    price: float

class UpdateProductRequest(BaseModel):
    product_name: Optional[str] = None
    price: Optional[float] = None

class CreateSellingRequest(BaseModel):
    id_client: str
    id_product: str
    price_at_moment: float

class UpdateSellingRequest(BaseModel):
    id_client: Optional[str] = None
    id_product: Optional[str] = None
    price_at_moment: Optional[float] = None
