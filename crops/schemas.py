from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PlantingCreate(BaseModel):
    crop_id: int
    season_id: int
    planting_date: datetime
    harvest_date: Optional[datetime] = None
    yield_amount: Optional[float] = None
    yield_quality: Optional[str] = None
    notes: Optional[str] = None

class PlantingUpdate(BaseModel):
    crop_id: Optional[int] = None
    season_id: Optional[int] = None
    planting_date: Optional[datetime] = None
    harvest_date: Optional[datetime] = None
    yield_amount: Optional[float] = None
    yield_quality: Optional[str] = None
    notes: Optional[str] = None

class PlantingOut(BaseModel):
    crop_id: int
    season_id: int
    planting_date: Optional[str] = None
    harvest_date: Optional[str] = None
    yield_amount: Optional[float] = None
    yield_quality: Optional[str] = None
    notes: Optional[str] = None

    class Config:
        from_attributes = True
