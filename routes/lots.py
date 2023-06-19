from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT, HTTP_205_RESET_CONTENT
from models.models import Lots, Supplies, Locations, Sub_locations, Projects, Suppliers
from schemas.lot_schema import LotListSchema, CreateLotSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

lots = APIRouter()


@lots.get("/api/lots", response_model=List[LotListSchema])
def get_lots(db: Session = Depends(get_db)):
    result = (
        db.query(
            Lots.id,
            Lots.number,
            Lots.due_date,
            Lots.stock,
            Lots.observations,
            Supplies.name.label("supply_name"),
            Supplies.code.label("supply_code"),
            Locations.name.label("location"),
            Sub_locations.name.label("sub_location"),
            Projects.name.label("project"),
        )
        .outerjoin(Supplies, Supplies.id == Lots.supplies_id)
        .outerjoin(Sub_locations, Sub_locations.id == Lots.sub_location_id)
        .outerjoin(Locations, Locations.id == Sub_locations.id)
        .outerjoin(Projects, Projects.id == Lots.project_id)
        .all()
    )
    return result


@lots.post("/api/lots", status_code=HTTP_201_CREATED)
def add_lots(lot: CreateLotSchema, db: Session = Depends(get_db)):
    new_lot = Lots(
        number=lot.number,
        due_date=lot.due_date,
        stock=lot.stock,
        observations=lot.observations,
        supplies_id=lot.supply_id,
        sub_location_id=lot.sub_location_id,
        project_id=lot.project_id,
        supplier_id = lot.supplier_id,
        state = True
    )
    db.add(new_lot)
    db.commit()
    db.refresh(new_lot)
    content = str(new_lot.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@lots.get("/api/lots/lot/{lot_id}", response_model=LotListSchema)
def get_lot(lot_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            Lots.id,
            Lots.number,
            Lots.due_date,
            Lots.stock,
            Lots.observations,
            Supplies.name.label("supply_name"),
            Supplies.code.label("supply_code"),
            Supplies.cost.label("supply_cost"),
            Locations.name.label("location"),
            Sub_locations.name.label("sub_location"),
            Projects.name.label("project"),
            Suppliers.name.label("supplier_name"),
        )
        .filter(Lots.id == lot_id and Lots.state == True)
        .outerjoin(Supplies, Supplies.id == Lots.supplies_id)
        .outerjoin(Sub_locations, Sub_locations.id == Lots.sub_location_id)
        .outerjoin(Locations, Locations.id == Sub_locations.id)
        .outerjoin(Projects, Projects.id == Lots.project_id)
        .outerjoin(Suppliers, Suppliers.id == Supplies.supplier_id)
        .first()
    )
    return result

@lots.get("/api/lots/supply/{supply_id}", response_model=List[LotListSchema])
def get_lots_supply(supply_id: int, db: Session = Depends(get_db)):
    result = (
        db.query(
            Lots.id,
            Lots.number,
            Lots.due_date,
            Lots.stock,
            Lots.observations,
            Locations.name.label("location"),
            Sub_locations.name.label("sub_location"),
            Projects.name.label("project"),
            Suppliers.name.label("supplier_name"),
        )
        .filter(Lots.supplies_id == supply_id, Lots.state == True)
        .outerjoin(Sub_locations, Sub_locations.id == Lots.sub_location_id)
        .outerjoin(Locations, Locations.id == Sub_locations.id)
        .outerjoin(Projects, Projects.id == Lots.project_id)
        .outerjoin(Suppliers, Suppliers.id == Lots.supplier_id)
        .all()
    )
    return result

@lots.put("/api/lots/{lot_id}", status_code=HTTP_205_RESET_CONTENT)
def deactive_lot(lot_id: int, db: Session = Depends(get_db)):
    db_lot = db.query(Lots).filter(Lots.id == lot_id).first()
    if not db_lot:
        return Response(status_code=HTTP_404_NOT_FOUND)
    setattr(db_lot, 'state', False)
    db.add(db_lot)
    db.commit()
    db.refresh(db_lot)
    return Response(status_code=HTTP_205_RESET_CONTENT)