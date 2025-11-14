from fastapi import APIRouter, HTTPException
from crops import crud
from crops.schemas import CropRotationCreate, CropRotationUpdate, CropRotationOut

router = APIRouter(prefix="/crops", tags=["Crops"])

@router.post("/", response_model=CropRotationOut)
def create_crop_rotation(crop: CropRotationCreate):
    try:
        new_crop = crud.create_crop_rotation(
            field_id=crop.field_id,
            crop_id=crop.crop_id,
            year=crop.year,
            season=crop.season,
            predecessor_crop_id=crop.predecessor_crop_id,
            notes=crop.notes,
            avg_yield=crop.avg_yield,
        )
        return new_crop
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[CropRotationOut])
def get_all():
    return crud.get_all_rotations()

@router.get("/{rotation_id}", response_model=CropRotationOut)
def get_one(rotation_id: int):
    rotation = crud.get_rotation(rotation_id)
    if not rotation:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return rotation

@router.get("/field/{field_id}", response_model=list[CropRotationOut])
def get_by_field(field_id: int):
    return crud.get_rotations_by_field(field_id)

@router.put("/{rotation_id}", response_model=CropRotationOut)
def update(rotation_id: int, data: CropRotationUpdate):
    updated = crud.update_rotation(rotation_id, data.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return updated

@router.delete("/{rotation_id}")
def delete(rotation_id: int):
    ok = crud.delete_rotation(rotation_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Запись не найдена")
    return {"message": "Культура удалена"}
