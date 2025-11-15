from fastapi import APIRouter, HTTPException, Depends

from auth.deps import get_current_user
from fields import crud
from fields.schemas import FieldCreate, FieldUpdate, FieldOut

router = APIRouter(prefix="/fields", tags=["Fields"])


@router.post("", response_model=FieldOut)
def create_field(field: FieldCreate, current_user=Depends(get_current_user)):
    try:
        new_field = crud.create_field(
            user_id=current_user.id,
            name=field.name,
            area_ha=field.area_ha,
            coordinates=field.coordinates,
            soil_type=field.soil_type,
        )

        return new_field

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[FieldOut])
def get_fields(current_user=Depends(get_current_user)):
    fields = crud.get_all_fields(owner_id=current_user.id)
    return fields

@router.get("/with/plantings")
def get_fields_with_plantings(current_user=Depends(get_current_user)):
    fields = crud.get_all_fields_with_plantings(owner_id=current_user.id)
    return fields


@router.get("/{field_id}", response_model=FieldOut)
def get_field(field_id: int, current_user=Depends(get_current_user)):
    field = crud.get_field(field_id, owner_id=current_user.id)
    if not field:
        raise HTTPException(status_code=404, detail="Поле не найдено")
    return field


@router.put("/{field_id}", response_model=FieldOut)
def update_field(field_id: int, field_update: FieldUpdate, current_user=Depends(get_current_user)):
    updated = crud.update_field(field_id, field_update.model_dump(exclude_unset=True), owner_id=current_user.id)
    if not updated:
        raise HTTPException(status_code=404, detail="Поле не найдено")
    return updated


@router.delete("/{field_id}")
def delete_field(field_id: int, current_user=Depends(get_current_user)):
    ok = crud.delete_field(field_id, owner_id=current_user.id)
    if not ok:
        raise HTTPException(status_code=404, detail="Поле не найдено")
    return {"message": "Поле успешно удалено"}
