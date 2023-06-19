from pydantic import BaseModel
from typing import Optional

class SupplierSupplySchema(BaseModel):
    supplier_id: int
    supply_id: int
    cost: int

    class Config:
        orm_mode = True

class GetSupplierSupplySchema(BaseModel):
    supplier_id: int
    supply_id: int
    cost: int
    name: str
    rut: str
    city_address: str

    class Config:
        orm_mode = True