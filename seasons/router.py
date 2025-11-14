from auth.deps import get_current_user
from fastapi import APIRouter, HTTPException, Depends

from seasons import crud
from seasons.schemas import SeasonCreate, SeasonUpdate, SeasonOut

router = APIRouter(prefix="/seasons", tags=["Seasons"])


@router.post("", response_model=SeasonOut)
def create_season(season: SeasonCreate, current_user=Depends(get_current_user)):
    try:
        new_season = crud.create_season(
            user_id=current_user.id,
            name=season.name,
            date_start=season.date_start,
            date_end=season.date_end
        )
        return {
            "id": new_season["id"],
            "name": new_season["name"],
            "date_start": new_season["date_start"],
            "date_end": new_season["date_end"],
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("", response_model=list[SeasonOut])
def get_seasons():
    Seasons = crud.get_all_seasons()
    return [
        {
            "id": f["id"],
            "name": f["name"],
            "date_start": f["date_start"],
            "date_end": f["date_end"],
        } for f in Seasons
    ]


@router.get("/{season_id}", response_model=SeasonOut)
def get_season(season_id: int):
    f = crud.get_season(season_id)
    if not f:
        raise HTTPException(status_code=404, detail="Сезон не найден")
    return f


@router.put("/{season_id}", response_model=SeasonOut)
def update_season(season_id: int, season_update: SeasonUpdate):
    updated = crud.update_season(season_id, season_update.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Сезон не найден")
    return updated


@router.delete("/{season_id}")
def delete_season(season_id: int):
    ok = crud.delete_season(season_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Сезон не найден")
    return {"message": "Сезон успешно удален"}
