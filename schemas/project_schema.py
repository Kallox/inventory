from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProjectSchema(BaseModel):
    id: Optional[int]
    name: str
    owner_id: Optional[int]

    class Config:
        orm_mode = True