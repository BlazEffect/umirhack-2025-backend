from fastapi import APIRouter, HTTPException, Depends
from backend.fields import crud
from backend.fields.schemas import FieldCreate, FieldUpdate, FieldOut
from backend.app.auth.deps import get_current_user  # импорт функции, которая извлекает юзера из токена
import json

router = APIRouter(prefix="/fields", tags=["Fields"])

@router.post("/", response_model=FieldOut)
def create_field(field: FieldCreate, current_user=Depends(get_current_user)):
    """Создание нового поля пользователем"""
    try:
        new_field = crud.create_field(
            user_id=current_user.id,
            name=field.name,
            area_ha=field.area_ha,
            points=[p.model_dump() for p in field.points],
            soil_type=field.soil_type,
        )
        return {
            "id": new_field["id"],
            "name": new_field["name"],
            "area_ha": new_field["area_ha"],
            "soil_type": new_field["soil_type"],
            "points": field.points
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[FieldOut])
def get_fields():
    fields = crud.get_all_fields()
    return [
        {
            "id": f["id"],
            "name": f["name"],
            "area_ha": f["area_ha"],
            "soil_type": f["soil_type"],
            "points": json.loads(f["coordinates"]) if f["coordinates"] else []
        } for f in fields
    ]

@router.get("/{field_id}", response_model=FieldOut)
def get_field(field_id: int):
    f = crud.get_field(field_id)
    if not f:
        raise HTTPException(status_code=404, detail="Поле не найдено")
    return f

@router.put("/{field_id}", response_model=FieldOut)
def update_field(field_id: int, field_update: FieldUpdate):
    updated = crud.update_field(field_id, field_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Поле не найдено")
    updated["points"] = json.loads(updated["coordinates"]) if updated["coordinates"] else []
    return updated

@router.delete("/{field_id}")
def delete_field(field_id: int):
    ok = crud.delete_field(field_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Поле не найдено")
    return {"message": "Поле успешно удалено"}
