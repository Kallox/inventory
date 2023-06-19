from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Supplies_types
from schemas.supplies_type_schema import SuppliesTypesSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

supplies_types = APIRouter()


@supplies_types.get("/api/supplies_types", response_model=List[SuppliesTypesSchema])
def get_supplies_types(db: Session = Depends(get_db)):
    result = db.query(Supplies_types.id, Supplies_types.name).all()
    return result


@supplies_types.post("/api/supplies_types", status_code=HTTP_201_CREATED)
def add_supplies_type(type: SuppliesTypesSchema, db: Session = Depends(get_db)):
    new_supplies_type = Supplies_types(name=type.name)
    db.add(new_supplies_type)
    db.commit()
    db.refresh(new_supplies_type)
    content = str(new_supplies_type.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
