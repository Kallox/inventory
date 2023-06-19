from typing import Optional
from pydantic import BaseModel
from datetime import date


class EquipmentSchema(BaseModel):
    id: Optional[int]
    name: str
    serial_number: Optional[str]
    umag_inventory_code: Optional[str]
    reception_date: date
    maintenance_period: Optional[int]
    last_preventive_mainteinance: Optional[date]
    observation: Optional[str]
    supplier_id: Optional[int]
    invoice_id: Optional[int]
    model_number_id: Optional[int]
    room_id: Optional[int]
    stage_id: Optional[int]

    class Config:
        orm_mode = True


class EquipmentListSchema(BaseModel):
    id: Optional[int]
    name: str
    serial_number: Optional[str]
    umag_inventory_code: Optional[str]
    reception_date: date
    maintenance_period: Optional[int]
    last_preventive_mainteinance: Optional[date]
    observation: Optional[str]
    room_id: Optional[int]
    room_name: Optional[str]
    supplier_id: Optional[int]
    supplier_name: Optional[str]
    invoice_id: Optional[int]
    invoice_number: Optional[int]
    model_number_id: Optional[int]
    model_number: Optional[str]

    class Config:
        orm_mode = True


class EquipmentFullSchema(BaseModel):
    id: Optional[int]
    name: str
    serial_number: Optional[str]
    umag_inventory_code: Optional[str]
    reception_date: date
    maintenance_period: Optional[int]
    observation: Optional[str]
    last_preventive_mainteinance: Optional[date]
    room_id: Optional[int]
    room_name: Optional[str]
    unit_id: Optional[int]
    unit_name: Optional[str]
    building_id: Optional[int]
    building_name: Optional[str]
    supplier_id: Optional[int]
    supplier_name: Optional[str]
    invoice_id: Optional[int]
    invoice_number: Optional[int]
    brand_id: Optional[int]
    brand_name: Optional[str]
    model_id: Optional[int]
    model_name: Optional[str]
    model_number_id: Optional[int]
    model_number: Optional[str]
    stage_id: Optional[int]
    stage_name: Optional[str]
    project_id: Optional[int]
    project_name: Optional[str]
    project_owner_id: Optional[str]
    project_owner_name: Optional[str]

    class Config:
        orm_mode = True


class UpdateEquipmentSchema(BaseModel):
    id: Optional[int]
    name: Optional[str]
    serial_number: Optional[str]
    umag_inventory_code: Optional[str]
    reception_date: Optional[date]
    maintenance_period: Optional[int]
    last_preventive_mainteinance: Optional[date]
    observation: Optional[str]
    supplier_id: Optional[int]
    invoice_id: Optional[int]
    model_number_id: Optional[int]
    room_id: Optional[int]
    stage_id: Optional[int]

    class Config:
        orm_mode = True
