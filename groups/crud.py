from pony.orm import db_session
from datetime import datetime
from db.models import FieldGroup, User, Field


@db_session
def create_group(user_id: int, name: str, description: str | None, rotation_group: str | None = None):
    user = User.get(id=user_id)
    if not user:
        raise ValueError("Пользователь не найден")

    group = FieldGroup(
        name=name,
        description=description,
        rotation_group=rotation_group,
        owner=user,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return field_group_to_dict(group)


@db_session
def get_all_groups_for_user(user_id: int):
    groups = FieldGroup.select(lambda g: g.owner.id == user_id)
    return [field_group_to_dict(g) for g in groups]


@db_session
def get_group_by_id(group_id: int):
    group = FieldGroup.get(id=group_id)
    return field_group_to_dict(group) if group else None


@db_session
def update_group(group_id: int, data: dict):
    group = FieldGroup.get(id=group_id)
    if not group:
        return None

    if "name" in data and data["name"]:
        group.name = data["name"]
    if "description" in data:
        group.description = data["description"]
    if "rotation_group" in data:
        group.rotation_group = data["rotation_group"]

    group.updated_at = datetime.utcnow()
    return field_group_to_dict(group)


@db_session
def delete_group(group_id: int):
    group = FieldGroup.get(id=group_id)
    if not group:
        return False

    # Удаляем связи с полями перед удалением группы
    group.fields.clear()
    group.delete()
    return True


@db_session
def add_field_to_group(group_id: int, field_id: int):
    """Добавить поле в группу"""
    group = FieldGroup.get(id=group_id)
    field = Field.get(id=field_id)

    if not group or not field:
        return False

    if field not in group.fields:
        group.fields.add(field)

    return True


@db_session
def remove_field_from_group(group_id: int, field_id: int):
    """Удалить поле из группы"""
    group = FieldGroup.get(id=group_id)
    field = Field.get(id=field_id)

    if not group or not field:
        return False

    if field in group.fields:
        group.fields.remove(field)

    return True


@db_session
def get_group_fields(group_id: int):
    """Получить все поля в группе"""
    group = FieldGroup.get(id=group_id)
    if not group:
        return []

    return [field_to_dict(field) for field in group.fields]


@db_session
def get_user_groups_with_fields(user_id: int):
    """Получить все группы пользователя с информацией о полях"""
    groups = FieldGroup.select(lambda g: g.owner.id == user_id)
    result = []

    for group in groups:
        group_data = field_group_to_dict(group)
        group_data['fields'] = [field_to_dict(field) for field in group.fields]
        group_data['fields_count'] = len(group.fields)
        result.append(group_data)

    return result


# Вспомогательные функции для преобразования в словари
def field_group_to_dict(group: FieldGroup) -> dict:
    """Преобразует объект FieldGroup в словарь для API"""
    if not group:
        return None

    return {
        "id": group.id,
        "name": group.name,
        "description": group.description,
        "rotation_group": group.rotation_group,
        "owner_id": group.owner.id if group.owner else None,
        "owner_username": group.owner.username if group.owner else None,
        "fields_count": len(group.fields) if group.fields else 0,
        "created_at": group.created_at.isoformat() if group.created_at else None,
        "updated_at": group.updated_at.isoformat() if group.updated_at else None
    }


def field_to_dict(field: Field) -> dict:
    """Преобразует объект Field в словарь для API"""
    if not field:
        return None

    return {
        "id": field.id,
        "name": field.name,
        "area_ha": field.area_ha,
        "soil_type": field.soil_type,
        "coordinates": field.coordinates,
        "owner_id": field.owner.id if field.owner else None
    }
