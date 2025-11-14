import json
from datetime import datetime, timezone

from pony.orm import db_session

from db.models import Field, User


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
    if "coordinates" in data and data["coordinates"]:
        updates["coordinates"] = json.dumps(data["coordinates"])
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
