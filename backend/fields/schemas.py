from pydantic import BaseModel, Field, field_validator
from typing import List, Optional

class Point(BaseModel):
    lat: float
    lon: float

class FieldCreate(BaseModel):
    name: str
    area_ha: float = Field(..., gt=0)
    points: List[Point] = Field(..., min_items=3)
    soil_type: Optional[str] = None

    @field_validator("points")
    def validate_points(cls, v):
        if len(v) < 3:
            raise ValueError("Поле должно содержать минимум 3 точки")
        return v

class FieldUpdate(BaseModel):
    name: Optional[str] = None
    area_ha: Optional[float] = Field(None, gt=0)
    points: Optional[List[Point]] = None
    soil_type: Optional[str] = None

class FieldOut(BaseModel):
    id: int
    name: str
    area_ha: float
    soil_type: Optional[str]
    points: List[Point]

    class Config:
        from_attributes = True
