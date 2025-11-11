from pony.orm import db_session, select
from backend.db.models import Season, User
from datetime import datetime
import json

@db_session
def create_season(user_id: int, owner: User, name: str, sowing_date: datetime, harvest_date: datetime, created_at: datetime, updated_at: datetime):
    # Проверяем, что пользователь существует
    user = User.get(id=user_id)
    if not user:
        raise ValueError("Пользователь не найден")

    # Создаем сезон
    season = Season(
        owner = owner,
        name=name,
        sowing_date=sowing_date,
        harvest_date=harvest_date,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
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
def update_season(season_id: int, data: dict):
    season = Season.get(id=season_id)
    if not season:
        return None

    if "name" in data and data["name"]:
        season.name = data["name"]
    if "sowing_date" in data and data["sowing_date"]:
        season.sowing_date = data["sowing_date"]
    if "harvest_date" in data and data["harvest_date"]:
        season.harvest_date = data["harvest_date"]

    season.updated_at = datetime.utcnow()
    return season.to_dict()

@db_session
def delete_season(season_id: int):
    season = Season.get(id=season_id)
    if not season:
        return False
    season.delete()
    return True
