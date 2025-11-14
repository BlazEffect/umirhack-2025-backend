from pony.orm import Database, PrimaryKey, Required, Optional
from datetime import datetime

db = Database()

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    email = Required(str, unique=True)
    username = Optional(str)
    hashed_password = Required(str)
    is_active = Required(bool, default=True)
    created_at = Required(datetime, default=lambda: datetime.utcnow())
