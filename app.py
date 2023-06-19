from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config.database import Base, engine
from routes.equipments import equipments
from routes.buildings import buildings
from routes.units import units
from routes.rooms import rooms
from routes.suppliers import suppliers
from routes.supplier_contact import suppliers_contacts
from routes.brands import brands
from routes.models import models
from routes.model_numbers import model_numbers
from routes.maintenances import maintenances
from routes.invoices import invoices
from routes.projects import projects
from routes.project_owners import project_owners
from routes.stages import stages
from routes.lots import lots
from routes.supplies import supplies
from routes.supplies_types import supplies_types
from routes.supplies_brands import supplies_brands
from routes.locations import locations
from routes.sub_locations import sub_locations
from routes.Suppliers_supplies import suppliers_supplies

def create_tables():
    #Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


create_tables()
app = FastAPI()
app.mount("/images", StaticFiles(directory="images"), name="images")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "PUT", "POST", "DELETE"],
    allow_headers=["*"],
)

routes = [
    buildings,
    brands,
    equipments,
    invoices,
    locations,
    lots,
    maintenances,
    models,
    model_numbers,
    units,
    projects,
    project_owners,
    rooms,
    stages,
    sub_locations,
    supplies,
    supplies_brands,
    supplies_types,
    suppliers,
    suppliers_contacts,
    suppliers_supplies,
]

for route in routes:
    app.include_router(route)
