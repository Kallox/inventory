from pydantic import BaseModel
from typing import Optional


class SubLocationSchema(BaseModel):
    id: Optional[int]
    name: str
    location_id: Optional[int]

    class Config:
        orm_mode = True
