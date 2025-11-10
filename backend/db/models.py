from datetime import datetime
from pony.orm import Database, Required, Optional, PrimaryKey, Set, Json

db = Database()

class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True)
    email = Required(str, unique=True)
    password_hash = Required(str)
    role = Required(str)  # 'owner', 'manager', 'viewer'
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)
    seasons = Set('Season')  # связь с сезонами пользователя — один ко многим
    # Поля (Field) не связаны напрямую с пользователями

class Season(db.Entity):
    id = PrimaryKey(int, auto=True)
    owner = Required(User)  # Пользователь-владелец сезона
    name = Required(str)  # Название сезона
    sowing_date = Required(datetime)  # Дата посева / начала сезона
    harvest_date = Required(datetime)  # Дата сбора / конца сезона
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)

class Field(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    area_ha = Required(float)
    coordinates = Optional(str)
    soil_type = Optional(str)
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)
    crop_rotations = Set('CropRotation')
    soil_profiles = Set('FieldSoilProfile')
    observations = Set('FieldObservation')
    irrigation_records = Set('IrrigationRecord')
    inputs_logs = Set('InputsLog')

class Crop(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    latin_name = Optional(str)
    crop_type = Optional(str)
    crop_rotations = Set('CropRotation')

class CropRotation(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)
    year = Required(int)
    season = Required(str)
    crop = Required(Crop)
    predecessor_crop = Optional(Crop)
    notes = Optional(str)
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)

class FieldSoilProfile(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)
    pH = Optional(float)
    organic_matter = Optional(float)
    nutrient_level = Optional(Json)
    moisture_content = Optional(float)
    sample_date = Optional(datetime)

class FieldObservation(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)
    date = Required(datetime)
    pest_pressure = Optional(int)
    disease_signs = Optional(str)
    yield_estimate = Optional(float)
    notes = Optional(str)

class IrrigationRecord(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)
    date = Required(datetime)
    amount_mm = Optional(float)
    method = Optional(str)
    operator = Optional(User)
    notes = Optional(str)

class InputsLog(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)
    date = Required(datetime)
    product = Required(str)
    amount = Required(float)
    unit = Required(str)
    supplier = Optional(str)

class AuditLog(db.Entity):
    id = PrimaryKey(int, auto=True)
    user = Required(User)
    action = Required(str)
    target = Optional(str)
    timestamp = Required(datetime, default=datetime.utcnow)
