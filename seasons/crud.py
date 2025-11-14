from datetime import datetime, timezone
from typing import Optional

from pony.orm import db_session

from db.models import Season, User


@db_session
def create_season(user_id: int, owner: User, name: str, date_start: datetime, date_end: datetime):
    user = User.get(id=user_id)
    if not user:
        raise ValueError("Пользователь не найден")

    season = Season(
        owner=owner,
        name=name,
        date_start=date_start,
        date_end=date_end,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )
    return season.to_dict()


@db_session
def get_all_seasons():
    return [f.to_dict() for f in Season.select()]


@db_session
def get_season(season_id: int):
    season = Season.get(id=season_id)
    if not season:
        return None
    data = season.to_dict()
    return data


@db_session
def update_season(season_id: int, data: dict) -> Optional[dict]:
    season = Season.get(id=season_id)
    if not season:
        return None

    updates = {}

    if name := data.get("name", "").strip():
        updates["name"] = name

    date_start = data.get("date_start")
    date_end = data.get("date_end")

    if date_start and date_end and date_start > date_end:
        raise ValueError("Дата начала не может быть позже даты окончания")

    if date_start:
        updates["date_start"] = date_start
    if date_end:
        updates["date_end"] = date_end

    if updates:
        updates["updated_at"] = datetime.now(timezone.utc)
        season.set(**updates)

    return season.to_dict()


@db_session
def delete_season(season_id: int):
    season = Season.get(id=season_id)
    if not season:
        return False
    season.delete()
    return True
