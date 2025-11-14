from pony.orm import db_session, select, desc
from datetime import datetime
from db.models import Planting, Field, Crop, Season


@db_session
def create_crop_rotation(field_id: int, crop_id: int, year: int, season: str, predecessor_crop_id: int | None,
                         notes: str | None, avg_yield: float | None):
    field = Field.get(id=field_id)
    crop = Crop.get(id=crop_id)
    if not field:
        raise ValueError("Поле не найдено")
    if not crop:
        raise ValueError("Культура не найдена")

    # Находим сезон по году (или создаем новый)
    season_obj = Season.get(season_year=year, name=season)
    if not season_obj:
        # Если сезон не найден, создаем его (нужен owner)
        # Для простоты берем первого пользователя или передавайте owner_id
        from db.models import User
        owner = User.select().first()
        if not owner:
            raise ValueError("Не найден пользователь для создания сезона")

        season_obj = Season(
            owner=owner,
            name=season,
            season_year=year,
            sowing_date=datetime(year, 1, 1),  # примерные даты
            harvest_date=datetime(year, 12, 31)
        )

    predecessor_crop = Crop.get(id=predecessor_crop_id) if predecessor_crop_id else None

    planting = Planting(
        field=field,
        crop=crop,
        season=season_obj,
        planting_date=datetime(year, 1, 1),  # примерная дата посадки
        yield_amount=avg_yield,
        notes=notes,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )

    return planting_to_dict(planting)


@db_session
def get_all_rotations():
    return [planting_to_dict(p) for p in Planting.select()]


@db_session
def get_rotation(rotation_id: int):
    planting = Planting.get(id=rotation_id)
    return planting_to_dict(planting) if planting else None


@db_session
def get_rotations_by_field(field_id: int):
    field = Field.get(id=field_id)
    if not field:
        return []
    return [planting_to_dict(p) for p in field.plantings]


@db_session
def update_rotation(rotation_id: int, data: dict):
    planting = Planting.get(id=rotation_id)
    if not planting:
        return None

    if "crop_id" in data and data["crop_id"]:
        planting.crop = Crop.get(id=data["crop_id"])
    if "year" in data and data["year"]:
        # Обновляем сезон
        year = data["year"]
        season_name = data.get("season", planting.season.name)
        season_obj = Season.get(season_year=year, name=season_name)
        if not season_obj:
            from db.models import User
            owner = User.select().first()
            season_obj = Season(
                owner=owner,
                name=season_name,
                season_year=year,
                sowing_date=datetime(year, 1, 1),
                harvest_date=datetime(year, 12, 31)
            )
        planting.season = season_obj
        planting.planting_date = datetime(year, 1, 1)  # обновляем дату посадки

    if "season" in data and data["season"]:
        planting.season.name = data["season"]

    if "predecessor_crop_id" in data:
        if data["predecessor_crop_id"]:
            planting.predecessor_crop = Crop.get(id=data["predecessor_crop_id"])
        else:
            planting.predecessor_crop = None

    if "notes" in data:
        planting.notes = data["notes"]

    if "avg_yield" in data:
        planting.yield_amount = data["avg_yield"]

    planting.updated_at = datetime.utcnow()
    return planting_to_dict(planting)


@db_session
def delete_rotation(rotation_id: int):
    planting = Planting.get(id=rotation_id)
    if not planting:
        return False
    planting.delete()
    return True


# Вспомогательная функция для преобразования Planting в словарь
def planting_to_dict(planting: Planting) -> dict:
    """Преобразует объект Planting в словарь для API"""
    if not planting:
        return None

    return {
        "id": planting.id,
        "field_id": planting.field.id if planting.field else None,
        "field_name": planting.field.name if planting.field else None,
        "crop_id": planting.crop.id if planting.crop else None,
        "crop_name": planting.crop.name if planting.crop else None,
        "season_id": planting.season.id if planting.season else None,
        "season_name": planting.season.name if planting.season else None,
        "season_year": planting.season.season_year if planting.season else None,
        "year": planting.season.season_year if planting.season else None,  # для обратной совместимости
        "season": planting.season.name if planting.season else None,  # для обратной совместимости
        "predecessor_crop_id": planting.predecessor_crop.id if planting.predecessor_crop else None,
        "predecessor_crop_name": planting.predecessor_crop.name if planting.predecessor_crop else None,
        "planting_date": planting.planting_date.isoformat() if planting.planting_date else None,
        "harvest_date": planting.harvest_date.isoformat() if planting.harvest_date else None,
        "yield_amount": planting.yield_amount,
        "yield_quality": planting.yield_quality,
        "notes": planting.notes,
        "created_at": planting.created_at.isoformat() if planting.created_at else None,
        "updated_at": planting.updated_at.isoformat() if planting.updated_at else None
    }


# Дополнительные функции для работы с новой структурой
@db_session
def get_planting_history(field_id: int, years_back: int = 5):
    """Получает историю посадок для поля"""
    field = Field.get(id=field_id)
    if not field:
        return []

    current_year = datetime.now().year
    plantings = select(
        p for p in Planting
        if p.field == field and
        p.season.season_year >= (current_year - years_back)
    ).order_by(lambda p: desc(p.season.season_year))

    return [planting_to_dict(p) for p in plantings]


@db_session
def create_planting_with_dates(field_id: int, crop_id: int, season_id: int,
                               planting_date: datetime, harvest_date: datetime = None,
                               yield_amount: float = None, yield_quality: str = None,
                               notes: str = None):
    """Создает посадку с точными датами"""
    field = Field.get(id=field_id)
    crop = Crop.get(id=crop_id)
    season = Season.get(id=season_id)

    if not field or not crop or not season:
        raise ValueError("Поле, культура или сезон не найдены")

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
