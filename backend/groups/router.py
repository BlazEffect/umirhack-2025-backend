from fastapi import APIRouter, HTTPException, Depends
from backend.groups import crud
from backend.groups.schemas import GroupCreate, GroupUpdate, GroupOut
from backend.auth.deps import get_current_user  # функция, которая достаёт пользователя из токена

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.post("/", response_model=GroupOut)
def create_group(group: GroupCreate, current_user=Depends(get_current_user)):
    """Создать группу, доступную во всех сезонах пользователя"""
    try:
        g = crud.create_group(
            user_id=current_user.id,
            name=group.name,
            description=group.description,
        )
        return {
            "id": g["id"],
            "name": g["name"],
            "description": g["description"],
            "owner_id": current_user.id,
            "created_at": g["created_at"],
            "updated_at": g["updated_at"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[GroupOut])
def list_groups(current_user=Depends(get_current_user)):
    groups = crud.get_all_groups_for_user(current_user.id)
    return [
        {
            "id": g["id"],
            "name": g["name"],
            "description": g["description"],
            "owner_id": g["owner"],
            "created_at": g["created_at"],
            "updated_at": g["updated_at"]
        } for g in groups
    ]

@router.get("/{group_id}", response_model=GroupOut)
def get_group(group_id: int):
    g = crud.get_group_by_id(group_id)
    if not g:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return g

@router.put("/{group_id}", response_model=GroupOut)
def update_group(group_id: int, data: GroupUpdate):
    g = crud.update_group(group_id, data.model_dump(exclude_unset=True))
    if not g:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return g

@router.delete("/{group_id}")
def delete_group(group_id: int):
    ok = crud.delete_group(group_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Группа не найдена")
    return {"message": "Группа удалена"}
