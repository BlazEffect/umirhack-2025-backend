from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class FieldCreate(BaseModel):
    name: str
    area_ha: float = Field(..., gt=0)
    coordinates: List[List[float]] = Field(..., min_items=3)
    soil_type: Optional[str] = None

    @field_validator("coordinates")
    @classmethod
    def validate_coordinates(cls, v: List[List[float]]) -> List[List[float]]:
        if len(v) < 3:
            raise ValueError("Поле должно содержать минимум 3 точки")

        for i, point in enumerate(v):
            if len(point) != 2:
                raise ValueError(f"Точка {i} должна содержать ровно 2 координаты")

        if v[0] != v[-1]:
            v.append(v[0])

        return v


class FieldUpdate(BaseModel):
    name: Optional[str] = None
    area_ha: Optional[float] = Field(None, gt=0)
    soil_type: Optional[str] = None


class FieldOut(BaseModel):
    id: int
    name: str
    area_ha: float
    soil_type: Optional[str]
    coordinates: List[List[float]]

    class Config:
        from_attributes = True
