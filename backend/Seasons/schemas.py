from pydantic import BaseModel
from typing import Optional
from datetime import date

class SeasonCreate(BaseModel):
    name: str
    date_start: date
    date_end: date

class SeasonUpdate(BaseModel):
    name: Optional[str] = None
    date_start: Optional[date] = None
    date_end: Optional[date] = None

class SeasonOut(BaseModel):
    id: int
    name: str
    date_start: date
    date_end: date
    class Config:
        from_attributes = True
