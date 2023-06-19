from pydantic import BaseModel
from typing import Optional
from datetime import date

class MaintenanceSchema(BaseModel):
    id: Optional[int]
    date: date
    observations: Optional[str]
    state: Optional[bool]
    maintenance_type: str
    equiptment_id: int

    class Config:
        orm_mode = True

class MaintenanceFromEquipment(BaseModel):
    id: int
    date: date
    observations: Optional[str]
    state: Optional[bool]
    maintenance_type: str

    class Config:
        orm_mode = True