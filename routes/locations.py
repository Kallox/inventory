from fastapi import APIRouter, Response, Depends
from starlette.status import HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from models.models import Locations
from schemas.location_schema import LocationSchema
from typing import List
from config.database import get_db
from sqlalchemy.orm import Session

locations = APIRouter()


@locations.get("/api/locations", response_model=List[LocationSchema])
def get_locations(db: Session = Depends(get_db)):
    result = db.query(Locations).all()
    return result


@locations.post("/api/locations", status_code=HTTP_201_CREATED)
def add_location(location: LocationSchema, db: Session = Depends(get_db)):
    new_location = Locations(name=location.name)
    db.add(new_location)
    db.commit()
    db.refresh(new_location)
    content = str(new_location.id)
    return Response(status_code=HTTP_201_CREATED, content=content)


@locations.get("/api/locations/{location_id}", response_model=LocationSchema)
def get_location(location_id: int, db: Session = Depends(get_db)):
    return db.query(Locations).filter(Locations.id == location_id).first()
