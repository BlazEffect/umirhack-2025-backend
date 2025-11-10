from pony.orm import db_session, select
from backend.db.models import Field, User
from datetime import datetime
import json

@db_session
def create_field(user_id: int, name: str, area_ha: float, points: list[dict], soil_type: str | None):
    # Проверяем, что пользователь существует
    user = User.get(id=user_id)
    if not user:
        raise ValueError("Пользователь не найден")

    # Создаем поле
    field = Field(
        name=name,
        area_ha=area_ha,
        coordinates=json.dumps(points),
        soil_type=soil_type,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return field.to_dict()

@db_session
def get_all_fields():
    return [f.to_dict() for f in Field.select()]

@db_session
def get_field(field_id: int):
    field = Field.get(id=field_id)
    if not field:
        return None
    data = field.to_dict()
    data["points"] = json.loads(field.coordinates) if field.coordinates else []
    return data

@db_session
def update_field(field_id: int, data: dict):
    field = Field.get(id=field_id)
    if not field:
        return None

    if "name" in data and data["name"]:
        field.name = data["name"]
    if "area_ha" in data and data["area_ha"]:
        field.area_ha = data["area_ha"]
    if "points" in data and data["points"]:
        field.coordinates = json.dumps(data["points"])
    if "soil_type" in data and data["soil_type"]:
        field.soil_type = data["soil_type"]

    field.updated_at = datetime.utcnow()
    return field.to_dict()

@db_session
def delete_field(field_id: int):
    field = Field.get(id=field_id)
    if not field:
        return False
    field.delete()
    return True
