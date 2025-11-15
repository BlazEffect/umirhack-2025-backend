from pydantic import BaseModel


class CalculatorRequest(BaseModel):
    culture: str
    area: float


class CalculatorResponse(BaseModel):
    seeds_cost: float
    fertilizers_cost: float
    revenue: float
    profit: float
