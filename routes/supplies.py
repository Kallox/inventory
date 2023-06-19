from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Supplies, Supplies_brand, Supplies_types, Suppliers
from schemas.supply_schema import SupplyListSchema, SupplySchema, UpdateStockSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import and_

supplies = APIRouter()


@supplies.get("/api/supplies", response_model=List[SupplyListSchema])
def get_supplies(db: Session = Depends(get_db)):
    result = (
        db.query(
            Supplies.id,
            Supplies.name,
            Supplies.code,
            Supplies.state,
            Supplies.stock,
            Supplies.samples,
            Supplies.critical_stock,
            Supplies_brand.name.label("supplies_brand_name"),
            Supplies_types.name.label("supplies_type_name"),
        )
        .outerjoin(Supplies_brand, Supplies_brand.id == Supplies.supplies_brand_id)
        .outerjoin(Supplies_types, Supplies_types.id == Supplies.supplies_type_id)
        .filter(Supplies.state == True)
        .all()
    )
    return result


@supplies.get("/api/supplies/critical", response_model=List[SupplyListSchema])
def get_supplies_critical(db: Session = Depends(get_db)):
    result = (
        db.query(
            Supplies.id,
            Supplies.name,
            Supplies.code,
            Supplies.stock,
            Supplies.samples,
            Supplies.critical_stock,
            Supplies_brand.name.label("supplies_brand_name"),
            Supplies_types.name.label("supplies_type_name"),
        )
        .outerjoin(Supplies_brand, Supplies_brand.id == Supplies.supplies_brand_id)
        .outerjoin(Supplies_types, Supplies_types.id == Supplies.supplies_type_id)
        .filter(and_(Supplies.stock <= Supplies.critical_stock, Supplies.state == True))
        .all()
    )
    return result


@supplies.post("/api/supplies", status_code=HTTP_201_CREATED)
def add_supplies(supply: SupplySchema, db: Session = Depends(get_db)):
    new_supply = Supplies(
        name=supply.name,
        code=supply.code,
        state=True,
        stock=supply.stock,
        samples=supply.samples,
        critical_stock=supply.critical_stock,
        supplies_brand_id=supply.supplies_brand_id,
        supplies_type_id=supply.supplies_type_id,
    )
    db.add(new_supply)
    db.commit()
    db.refresh(new_supply)
    content = str(new_supply.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@supplies.get("/api/supplies/{supply_id}", response_model=SupplyListSchema)
def get_supply(supply_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            Supplies.id,
            Supplies.name,
            Supplies.code,
            Supplies.state,
            Supplies.stock,
            Supplies.critical_stock,
            Supplies.samples,
            Supplies_brand.name.label("supplies_brand_name"),
            Supplies_types.name.label("supplies_type_name"),
        )
        .filter(and_(Supplies.id == supply_id, Supplies.state == True))
        .outerjoin(Supplies_brand, Supplies_brand.id == Supplies.supplies_brand_id)
        .outerjoin(Supplies_types, Supplies_types.id == Supplies.supplies_type_id)
        .first()
    )
    if result == None:
        return Response(status_code=HTTP_404_NOT_FOUND)
    return result


@supplies.put("/api/supplies/{supply_id}", response_model=SupplySchema)
def update_stock(
    data_update: UpdateStockSchema, supply_id: int, db: Session = Depends(get_db)
):
    db_supply = db.query(Supplies).filter(Supplies.id == supply_id).first()
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    setattr(db_supply, "stock", db_supply.stock + data_update.stock)
    db.add(db_supply)
    db.commit()
    db.refresh(db_supply)
    return db_supply


@supplies.delete("/api/supplies/{supply_id}", status_code=HTTP_204_NO_CONTENT)
def delete_supply(supply_id: int, db: Session = Depends(get_db)):
    db_supply = db.query(Supplies).filter(Supplies.id == supply_id).first()
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    setattr(db_supply, "state", False)
    db.add(db_supply)
    db.commit()
    db.refresh(db_supply)
    return db_supply
