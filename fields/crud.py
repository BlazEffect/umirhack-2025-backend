import json
from datetime import datetime, timezone

from pony.orm import db_session, select

from db.models import Field, User, Planting, Crop


@db_session
def create_field(user_id: int, name: str, area_ha: float, coordinates: list[list], soil_type: str | None):
    user = User.get(id=user_id)
    if not user:
        raise ValueError("Пользователь не найден")

    field = Field(
        name=name,
        owner=user,
        area_ha=area_ha,
        coordinates=json.dumps(coordinates),
        soil_type=soil_type,
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc)
    )

    result = field.to_dict()

    if "coordinates" in result and isinstance(result["coordinates"], str):
        result["coordinates"] = json.loads(result["coordinates"])

    return result


@db_session
def get_all_fields(owner_id: int):
    fields = Field.select(lambda f: f.owner.id == owner_id)
    result = []
    for field in fields:
        field_data = field.to_dict()
        if "coordinates" in field_data and isinstance(field_data["coordinates"], str):
            field_data["coordinates"] = json.loads(field_data["coordinates"])
        result.append(field_data)
    return result


@db_session
def get_all_fields_with_plantings(owner_id: int):
    # Сначала получаем все поля
    fields = Field.select(lambda f: f.owner.id == owner_id)[:]

    # Получаем все посадки для этих полей одним запросом
    field_ids = [f.id for f in fields]
    plantings = select(
        p for p in Planting
        if p.field.id in field_ids
    )[:]

    # Получаем все культуры и семейства для этих посадок
    planting_ids = [p.id for p in plantings]
    crop_ids = [p.crop.id for p in plantings if p.crop]

    # Prefetch для культур и их семейств
    crops = select(c for c in Crop if c.id in crop_ids).prefetch(Crop.family)[:]

    # Создаем словари для быстрого доступа
    crops_dict = {crop.id: crop for crop in crops}
    plantings_by_field = {}

    for planting in plantings:
        field_id = planting.field.id
        if field_id not in plantings_by_field:
            plantings_by_field[field_id] = []
        plantings_by_field[field_id].append(planting)

    result = []

    for field in fields:
        field_plantings = []

        for planting in plantings_by_field.get(field.id, []):
            crop = crops_dict.get(planting.crop.id) if planting.crop else None
            season = planting.season

            planting_dict = {
                'id': planting.id,
                'crop_id': crop.id if crop else None,
                'crop_name': crop.name if crop else None,
                'crop_family': crop.family.name if crop and crop.family else None,
                'year': season.date_start.year if season and season.date_start else None,
                'season': season.name if season else None,
                'planting_date': planting.planting_date,
                'harvest_date': planting.harvest_date,
                'yield_amount': planting.yield_amount,
                'yield_quality': planting.yield_quality,
                'notes': planting.notes,
            }
            field_plantings.append(planting_dict)

        coordinates = field.coordinates
        if coordinates and isinstance(coordinates, str):
            try:
                coordinates = json.loads(coordinates)
            except json.JSONDecodeError:
                coordinates = None

        field_data = {
            'id': field.id,
            'name': field.name,
            'area_ha': field.area_ha,
            'soil_type': field.soil_type,
            'coordinates': coordinates,
            'plantings': field_plantings,
        }

        result.append(field_data)

    return result


@db_session
def get_field(field_id: int, owner_id: int):
    field = Field.get(id=field_id, owner=owner_id)
    if not field:
        return None
    data = field.to_dict()
    if "coordinates" in data and isinstance(data["coordinates"], str):
        data["coordinates"] = json.loads(data["coordinates"])
    return data


@db_session
def update_field(field_id: int, data: dict, owner_id: int):
    field = Field.get(id=field_id, owner=owner_id)
    if not field:
        return None

    updates = {}

    if "name" in data and data["name"]:
        updates["name"] = data["name"]
    if "area_ha" in data and data["area_ha"]:
        updates["area_ha"] = data["area_ha"]
    if "soil_type" in data:
        updates["soil_type"] = data["soil_type"]

    if updates:
        updates["updated_at"] = datetime.now(timezone.utc)
        field.set(**updates)

    result = field.to_dict()
    if "coordinates" in result and isinstance(result["coordinates"], str):
        result["coordinates"] = json.loads(result["coordinates"])
    return result


@db_session
def delete_field(field_id: int, owner_id: int):
    field = Field.get(id=field_id, owner=owner_id)
    if not field:
        return False
    field.delete()
    return True
