from datetime import timedelta, date
from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Response, Depends, UploadFile
from fastapi.responses import FileResponse
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import (
    Equipments,
    Suppliers,
    Invoices,
    Model_numbers,
    Rooms,
    Units,
    Buildings,
    Maintenances,
    Brands,
    Models,
    Stages,
    Projects,
    Project_owners,
)
from schemas.equipment_schema import (
    EquipmentSchema,
    EquipmentFullSchema,
    EquipmentListSchema,
    UpdateEquipmentSchema,
)
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session
import os
import shutil

from routes.suppliers import get_supplier
from routes.invoices import get_invoice
from routes.model_numbers import get_model_number
from routes.rooms import get_room
from routes.stages import get_stage

equipments = APIRouter()


@equipments.get("/api/equipments", response_model=List[EquipmentListSchema])
def get_equipments(db: Session = Depends(get_db)):
    result = (
        db.query(
            Equipments.id,
            Equipments.name,
            Equipments.serial_number,
            Equipments.umag_inventory_code,
            Equipments.reception_date,
            Equipments.maintenance_period,
            Equipments.observation,
            Equipments.room_id,
            Rooms.name.label("room_name"),
            Equipments.supplier_id,
            Suppliers.name.label("supplier_name"),
            Equipments.invoice_id,
            Invoices.number.label("invoice_number"),
            Equipments.model_number_id,
            Model_numbers.number.label("model_number"),
        )
        .outerjoin(Rooms, Rooms.id == Equipments.room_id)
        .outerjoin(Suppliers, Suppliers.id == Equipments.supplier_id)
        .outerjoin(Invoices, Invoices.id == Equipments.invoice_id)
        .outerjoin(Model_numbers, Model_numbers.id == Equipments.model_number_id)
        .all()
    )
    return result


@equipments.get(
    "/api/equipments/nextmaintenances", response_model=List[EquipmentSchema]
)
def get_equipments_nextmaintenances(db: Session = Depends(get_db)):
    return (
        db.query(Equipments)
        .filter(
            Equipments.last_preventive_mainteinance + relativedelta(months=+Equipments.maintenance_period)
            == date.today() - timedelta(30)
        )
        .all()
    )


@equipments.post("/api/equipments", status_code=HTTP_201_CREATED)
def add_equipment(equipment: EquipmentSchema, db: Session = Depends(get_db)):
    if equipment.supplier_id != None:
        db_supplier = get_supplier(equipment.supplier_id, db=db)
        if not db_supplier:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.invoice_id != None:
        db_invoice = get_invoice(equipment.invoice_id, db=db)
        if not db_invoice:
            print("No se encontro el invoice", equipment.invoice_id)
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.model_number_id != None:
        db_model_number = get_model_number(equipment.model_number_id, db=db)
        if not db_model_number:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.room_id != None:
        db_room = get_room(equipment.room_id, db=db)
        if not db_room:
            return Response(status_code=HTTP_404_NOT_FOUND)
    if equipment.stage_id != None:
        db_stage = get_stage(equipment.stage_id, db=db)
        if not db_stage:
            return Response(status_code=HTTP_404_NOT_FOUND)

    new_equipment = Equipments(
        name=equipment.name,
        serial_number=equipment.serial_number,
        umag_inventory_code=equipment.umag_inventory_code,
        reception_date=equipment.reception_date,
        maintenance_period=equipment.maintenance_period,
        observation=equipment.observation,
        last_preventive_mainteinance=equipment.last_preventive_mainteinance,
        supplier_id=equipment.supplier_id,
        invoice_id=equipment.invoice_id,
        model_number_id=equipment.model_number_id,
        room_id=equipment.room_id,
        stage_id=equipment.stage_id,
    )
    db.add(new_equipment)
    db.commit()
    db.refresh(new_equipment)
    content = str(new_equipment.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


# Upload image to equipments folder using invoice id
@equipments.post("/api/equipments/{equipment_id}", status_code=HTTP_201_CREATED)
async def add_image(equipment_id: int, file: UploadFile):
    if not os.path.exists(f"./images/equipments/{equipment_id}"):
        os.makedirs(f"./images/equipments/{equipment_id}")
    with open(f"./images/equipments/{equipment_id}/{file.filename}", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return Response(status_code=HTTP_201_CREATED)


# Get images from equipments folder
@equipments.get("/api/equipments/image/{equipment_id}")
async def get_images(equipment_id: int):
    image_dir = f"/images/equipments/{equipment_id}"
    if not os.path.exists("." + image_dir):
        return Response(status_code=HTTP_404_NOT_FOUND)
    response = []
    files = os.listdir("." + image_dir)
    count = 1
    for file in files:
        image = {
            "id": count,
            "name": file,
            "path": f"http://localhost:8000{image_dir}/{file}",
        }
        count = count + 1
        response.append(image)
    return response


@equipments.get("/api/equipments/{equipment_id}", response_model=EquipmentFullSchema)
def get_equipment(equipment_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            Equipments.id,
            Equipments.name,
            Equipments.serial_number,
            Equipments.umag_inventory_code,
            Equipments.reception_date,
            Equipments.maintenance_period,
            Equipments.observation,
            Equipments.room_id,
            Rooms.name.label("room_name"),
            Equipments.supplier_id,
            Suppliers.name.label("supplier_name"),
            Equipments.invoice_id,
            Invoices.number.label("invoice_number"),
            Brands.id.label("brand_id"),
            Brands.name.label("brand_name"),
            Models.id.label("model_id"),
            Models.name.label("model_name"),
            Equipments.model_number_id,
            Model_numbers.number.label("model_number"),
            Units.id.label("unit_id"),
            Units.name.label("unit_name"),
            Buildings.id.label("building_id"),
            Buildings.name.label("building_name"),
            Stages.id.label("stage_id"),
            Stages.name.label("stage_name"),
            Projects.id.label("project_id"),
            Projects.name.label("project_name"),
            Project_owners.id.label("project_owner_id"),
            Project_owners.name.label("project_owner_name"),
        )
        .outerjoin(Rooms, Rooms.id == Equipments.room_id)
        .outerjoin(Suppliers, Suppliers.id == Equipments.supplier_id)
        .outerjoin(Invoices, Invoices.id == Equipments.invoice_id)
        .outerjoin(Model_numbers, Model_numbers.id == Equipments.model_number_id)
        .outerjoin(Models, Models.id == Model_numbers.id)
        .outerjoin(Brands, Brands.id == Models.brand_id)
        .outerjoin(Units, Units.id == Rooms.unit_id)
        .outerjoin(Buildings, Buildings.id == Units.building_id)
        .outerjoin(Stages, Stages.id == Equipments.stage_id)
        .outerjoin(Projects, Projects.id == Stages.project_id)
        .outerjoin(Project_owners, Project_owners.id == Projects.owner_id)
        .filter(Equipments.id == equipment_id)
        .first()
    )
    return result


@equipments.get("/api/equipment/{equipment_id}", response_model=EquipmentSchema)
def get_equipment_exist(equipment_id: int, db: Session = Depends(get_db)):
    return db.query(Equipments).filter(Equipments.id == equipment_id).first()


@equipments.delete("/api/equipments/{equipment_id}", status_code=HTTP_204_NO_CONTENT)
def delete_equipment(equipment_id: int, db: Session = Depends(get_db)):
    db_equipment = db.query(Equipments).filter(Equipments.id == equipment_id).first()
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db.delete(db_equipment)
    db.commit()
    return Response(status_code=HTTP_204_NO_CONTENT)


@equipments.put("/api/equipments/{equipment_id}", response_model=UpdateEquipmentSchema)
def update_equipment(
    data_update: UpdateEquipmentSchema, equipment_id: int, db: Session = Depends(get_db)
):
    db_equipment = db.query(Equipments).filter(Equipments.id == equipment_id).first()
    if not db_equipment:
        return Response(status_code=HTTP_404_NOT_FOUND)
    for key, value in data_update.dict(exclude_unset=True).items():
        setattr(db_equipment, key, value)
    db.add(db_equipment)
    db.commit()
    db.refresh(db_equipment)
    return db_equipment
