from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SeasonCreate(BaseModel):
    name: str
    date_start: datetime
    date_end: datetime

class SeasonUpdate(BaseModel):
    name: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None

class SeasonOut(BaseModel):
    id: int
    name: str
    date_start: datetime
    date_end: datetime
    class Config:
        from_attributes = True
