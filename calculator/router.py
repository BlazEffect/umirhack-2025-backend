from fastapi import FastAPI, HTTPException, APIRouter, Query

from calculator.calculator import EconomicCalculator
from calculator.schemas import CalculatorResponse, CalculatorRequest

router = APIRouter(prefix="/calculator", tags=["Calculator"])
calculator = EconomicCalculator()


@router.get("/calc")
def calculate(
    culture: str = Query(..., description="Название культуры: пшеница, кукуруза, соя"),
    area: float = Query(..., gt=0, description="Площадь в гектарах"),
    avg_yield_cq: float = Query(..., gt=0, description="Средняя урожаеность")
):
    try:
        result = calculator.calculate(culture, area, avg_yield_cq)
        return {
            "culture": culture,
            "area": area,
            "result": result
        }
    except Exception as e:
        return {"error": str(e)}
