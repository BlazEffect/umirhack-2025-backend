from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class CropRotationBase(BaseModel):
    field_id: int
    crop_id: int
    year: int = Field(..., ge=1900, le=2100)
    season: str
    predecessor_crop_id: Optional[int] = None
    notes: Optional[str] = None
    avg_yield: Optional[float] = Field(None, ge=0)

class CropRotationCreate(CropRotationBase):
    pass

class CropRotationUpdate(BaseModel):
    crop_id: Optional[int] = None
    year: Optional[int] = None
    season: Optional[str] = None
    predecessor_crop_id: Optional[int] = None
    notes: Optional[str] = None
    avg_yield: Optional[float] = Field(None, ge=0)

class CropRotationOut(CropRotationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
