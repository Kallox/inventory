from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Suppliers_has_Supplies, Suppliers, Supplies
from schemas.supplier_supply_schema import SupplierSupplySchema, GetSupplierSupplySchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

suppliers_supplies = APIRouter()


@suppliers_supplies.get(
    "/api/suppliers_supplies", response_model=List[SupplierSupplySchema]
)
def get_suppliers_supplies(db: Session = Depends(get_db)):
    result = db.query(Suppliers_has_Supplies).all()
    return result


@suppliers_supplies.post("/api/suppliers_supplies", status_code=HTTP_201_CREATED)
def add_supplier_supply(
    supplier_supply: SupplierSupplySchema, db: Session = Depends(get_db)
):
    db_supplier = (
        db.query(Suppliers).filter(Suppliers.id == supplier_supply.supplier_id).first()
    )
    if not db_supplier:
        return Response(status_code=HTTP_404_NOT_FOUND)
    db_supply = (
        db.query(Supplies).filter(Supplies.id == supplier_supply.supply_id).first()
    )
    if not db_supply:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_supplier_supply = Suppliers_has_Supplies(
        supplier_id=supplier_supply.supplier_id, supply_id=supplier_supply.supply_id, cost=supplier_supply.cost
    )
    db.add(new_supplier_supply)
    db.commit()
    db.refresh(new_supplier_supply)
    return Response(status_code=HTTP_201_CREATED)


@suppliers_supplies.get(
    "/api/suppliers_supplies/{supply_id}", response_model=List[GetSupplierSupplySchema]
)
def get_suppliers_supply(supply_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            Suppliers_has_Supplies.supplier_id,
            Suppliers_has_Supplies.supply_id,
            Suppliers_has_Supplies.cost,
            Suppliers.name.label("name"),
            Suppliers.rut.label("rut"),
            Suppliers.city_address.label("city_address"),
        )
        .filter(Suppliers_has_Supplies.supply_id == supply_id)
        .outerjoin(Suppliers, Suppliers.id == Suppliers_has_Supplies.supplier_id)
        .all()
    )
    return result
