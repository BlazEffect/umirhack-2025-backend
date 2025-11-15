from fastapi import APIRouter, HTTPException, Depends

from crops import crud
from crops.schemas import PlantingCreate, PlantingUpdate, PlantingOut

router = APIRouter(prefix="/fields/{field_id}/plantings", tags=["Plantings"])


@router.post("", response_model=PlantingOut)
def create_planting(
        field_id: int,
        planting: PlantingCreate,
):
    try:
        new_planting = crud.create_planting_with_dates(
            field_id=field_id,
            crop_id=planting.crop_id,
            season_id=planting.season_id,
            planting_date=planting.planting_date,
            harvest_date=planting.harvest_date,
            yield_amount=planting.yield_amount,
            yield_quality=planting.yield_quality,
            notes=planting.notes,
        )
        return new_planting
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[PlantingOut])
def get_all_plantings(field_id: int):
    return crud.get_plantings_by_field(field_id)


@router.get("/{planting_id}", response_model=PlantingOut)
def get_planting(field_id: int, planting_id: int):
    planting = crud.get_planting(planting_id)
    if not planting or planting.get('field_id') != field_id:
        raise HTTPException(status_code=404, detail="Посадка не найдена")
    return planting


@router.put("/{planting_id}", response_model=PlantingOut)
def update_planting(field_id: int, planting_id: int, data: PlantingUpdate):
    # Проверяем существование и принадлежность записи
    existing = crud.get_planting(planting_id)
    if not existing or existing.get('field_id') != field_id:
        raise HTTPException(status_code=404, detail="Посадка не найдена")

    updated = crud.update_planting(planting_id, data.model_dump(exclude_unset=True))
    return updated


@router.delete("/{planting_id}")
def delete_planting(field_id: int, planting_id: int):
    # Проверяем существование и принадлежность записи
    existing = crud.get_planting(planting_id)
    if not existing or existing.get('field_id') != field_id:
        raise HTTPException(status_code=404, detail="Посадка не найдена")

    ok = crud.delete_planting(planting_id)
    return {"message": "Посадка удалена"}
