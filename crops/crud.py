from pony.orm import db_session, select, desc
from datetime import datetime
from db.models import Planting, Field, Crop, Season

@db_session
def create_planting_with_dates(
    field_id: int,
    crop_id: int,
    season_id: int,
    planting_date: datetime,
    harvest_date: datetime = None,
    yield_amount: float = None,
    yield_quality: str = None,
    notes: str = None
):
    field = Field.get(id=field_id)
    crop = Crop.get(id=crop_id)
    season = Season.get(id=season_id)

    if not field:
        raise ValueError("Поле не найдено")
    if not crop:
        raise ValueError("Культура не найдена")
    if not season:
        raise ValueError("Сезон не найден")

    planting = Planting(
        field=field,
        crop=crop,
        season=season,
        planting_date=planting_date,
        harvest_date=harvest_date,
        yield_amount=yield_amount,
        yield_quality=yield_quality,
        notes=notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    return planting_to_dict(planting)

@db_session
def update_planting(planting_id: int, data: dict):
    planting = Planting.get(id=planting_id)
    if not planting:
        return None

    if "crop_id" in data and data["crop_id"]:
        crop = Crop.get(id=data["crop_id"])
        if crop:
            planting.crop = crop

    if "season_id" in data and data["season_id"]:
        season = Season.get(id=data["season_id"])
        if season:
            planting.season = season

    if "planting_date" in data:
        planting.planting_date = data["planting_date"]

    if "harvest_date" in data:
        planting.harvest_date = data["harvest_date"]

    if "yield_amount" in data:
        planting.yield_amount = data["yield_amount"]

    if "yield_quality" in data:
        planting.yield_quality = data["yield_quality"]

    if "notes" in data:
        planting.notes = data["notes"]

    planting.updated_at = datetime.utcnow()
    return planting_to_dict(planting)

# Переименуйте существующие функции для consistency
@db_session
def get_all_plantings():
    return [planting_to_dict(p) for p in Planting.select()]

@db_session
def get_planting(planting_id: int):
    planting = Planting.get(id=planting_id)
    return planting_to_dict(planting) if planting else None

@db_session
def get_plantings_by_field(field_id: int):
    field = Field.get(id=field_id)
    if not field:
        return []
    return [planting_to_dict(p) for p in field.plantings]

@db_session
def delete_planting(planting_id: int):
    planting = Planting.get(id=planting_id)
    if not planting:
        return False
    planting.delete()
    return True

def planting_to_dict(planting: Planting) -> dict:
    """Преобразует объект Planting в словарь для API"""
    if not planting:
        return None

    return {
        'id': planting.id,  # ID посадки, а не культуры
        'field_id': planting.field.id,  # добавьте field_id
        'crop_id': planting.crop.id,  # ID культуры
        'season_id': planting.season.id,  # ID сезона
        'planting_date': planting.planting_date.isoformat() if planting.planting_date else None,  # преобразовать в строку
        'harvest_date': planting.harvest_date.isoformat() if planting.harvest_date else None,  # преобразовать в строку
        'yield_amount': planting.yield_amount,
        'yield_quality': planting.yield_quality,
        'notes': planting.notes,
    }
