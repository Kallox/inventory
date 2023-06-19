from typing import Optional
from pydantic import BaseModel


class SupplyListSchema(BaseModel):
    id: int
    name: str
    code: Optional[str]
    state: Optional[bool]
    stock: Optional[int]
    critical_stock: Optional[int]
    samples: Optional[float]
    supplies_brand_name: Optional[str]
    supplies_type_name: Optional[str]

    class Config:
        orm_mode = True


class SupplySchema(BaseModel):
    id: Optional[int]
    name: str
    code: Optional[str]
    state: Optional[bool]
    stock: Optional[int]
    critical_stock: Optional[int]
    samples: Optional[float]
    supplies_brand_id: Optional[int]
    supplies_type_id: Optional[int]

    class Config:
        orm_mode = True

class UpdateStockSchema(BaseModel):
    stock: int

    class Config:
        orm_mode = True