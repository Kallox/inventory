from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Sub_locations, Locations
from schemas.sub_location_schema import SubLocationSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

sub_locations = APIRouter()


@sub_locations.get("/api/sub_locations", response_model=List[SubLocationSchema])
def get_sub_locations(db: Session = Depends(get_db)):
    result = db.query(Sub_locations).all()
    return result


@sub_locations.post("/api/sub_locations", status_code=HTTP_201_CREATED)
def add_sub_location(sub_location: SubLocationSchema, db: Session = Depends(get_db)):
    db_location = (
        db.query(Locations).filter(Locations.id == sub_location.location_id).first()
    )
    if not db_location:
        return Response(status_code=HTTP_404_NOT_FOUND)
    new_sub_location = Sub_locations(
        name=sub_location.name, location_id=sub_location.location_id
    )
    db.add(new_sub_location)
    db.commit()
    db.refresh(new_sub_location)
    content = str(new_sub_location.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@sub_locations.get(
    "/api/sub_locations/{location_id}", response_model=List[SubLocationSchema]
)
def get_sub_locations_locations(location_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Sub_locations).filter(Sub_locations.location_id == location_id).all()
    )
