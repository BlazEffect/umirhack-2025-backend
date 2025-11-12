from pony.orm import db_session, select
from datetime import datetime
from backend.db.models import Group, User

@db_session
def create_group(user_id: int, name: str, description: str | None):
    user = User.get(id=user_id)
    if not user:
        raise ValueError("Пользователь не найден")

    group = Group(
        name=name,
        description=description,
        owner=user,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    return group.to_dict()

@db_session
def get_all_groups_for_user(user_id: int):
    return [g.to_dict() for g in Group.select(lambda g: g.owner.id == user_id)]

@db_session
def get_group_by_id(group_id: int):
    group = Group.get(id=group_id)
    return group.to_dict() if group else None

@db_session
def update_group(group_id: int, data: dict):
    group = Group.get(id=group_id)
    if not group:
        return None

    if "name" in data and data["name"]:
        group.name = data["name"]
    if "description" in data:
        group.description = data["description"]

    group.updated_at = datetime.utcnow()
    return group.to_dict()

@db_session
def delete_group(group_id: int):
    group = Group.get(id=group_id)
    if not group:
        return False
    group.delete()
    return True
