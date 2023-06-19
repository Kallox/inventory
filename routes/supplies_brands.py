from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Supplies_brand
from schemas.supplies_brand_schema import SuppliesBrandsSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

supplies_brands = APIRouter()


@supplies_brands.get("/api/supplies_brands", response_model=List[SuppliesBrandsSchema])
def get_supplies_brands(db: Session = Depends(get_db)):
    result = db.query(Supplies_brand.id, Supplies_brand.name).all()
    return result


@supplies_brands.post("/api/supplies_brands", status_code=HTTP_201_CREATED)
def add_supplies_brand(brand: SuppliesBrandsSchema, db: Session = Depends(get_db)):
    new_supplies_brand = Supplies_brand(name=brand.name)
    db.add(new_supplies_brand)
    db.commit()
    db.refresh(new_supplies_brand)
    content = str(new_supplies_brand.id)
    return Response(status_code=HTTP_201_CREATED, content=content)
