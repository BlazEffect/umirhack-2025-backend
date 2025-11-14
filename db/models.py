import os
from datetime import datetime

from dotenv import load_dotenv
from pony.orm import Database
from pony.orm import Required, Optional, PrimaryKey, Set, Json

load_dotenv()

db = Database()
db.bind(
    provider="postgres",
    user=os.getenv("POSTGRES_USER", "postgres"),
    password=os.getenv("POSTGRES_PASSWORD", "postgres"),
    host=os.getenv("POSTGRES_HOST", "localhost"),
    database=os.getenv("POSTGRES_DB", "farmdb"),
    port=os.getenv("POSTGRES_PORT", "5432"),
)


class User(db.Entity):
    id = PrimaryKey(int, auto=True)
    username = Required(str, unique=True, max_len=50)
    email = Required(str, unique=True, max_len=100)
    password_hash = Required(str, max_len=255)
    role = Required(str, max_len=20)  # 'owner', 'manager', 'viewer'
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)

    # Связи
    seasons = Set('Season')
    field_groups = Set('FieldGroup')
    fields = Set('Field')
    irrigation_records = Set('IrrigationRecord')


class Season(db.Entity):
    id = PrimaryKey(int, auto=True)
    owner = Required(User)
    name = Required(str, max_len=100)
    date_start = Required(datetime)
    date_end = Required(datetime)
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)

    # Связи
    plantings = Set('Planting')


class FieldGroup(db.Entity):
    id = PrimaryKey(int, auto=True)
    owner = Required(User)
    name = Required(str, max_len=100)
    description = Optional(str)
    rotation_group = Optional(str, max_len=50)  # 'heavy_feeders', 'legumes', 'roots', 'potatoes'
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)

    # Связи многие-ко-многим с полями
    fields = Set('Field')


class Field(db.Entity):
    id = PrimaryKey(int, auto=True)
    owner = Required(User)
    name = Required(str, max_len=100)
    area_ha = Required(float)
    coordinates = Optional(str)  # JSON или WKT
    soil_type = Optional(str, max_len=50)
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)

    # Связи
    groups = Set(FieldGroup)  # многие-ко-многим
    soil_profiles = Set('FieldSoilProfile')
    observations = Set('FieldObservation')
    irrigation_records = Set('IrrigationRecord')
    inputs_logs = Set('InputsLog')
    plantings = Set('Planting')
    rotation_recommendations = Set('RotationRecommendation')


class PlantFamily(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True, max_len=50)
    latin_name = Optional(str, max_len=100)
    description = Optional(str)

    # Связи
    crops = Set('Crop')


class AppetiteLevel(db.Entity):
    id = PrimaryKey(int, auto=True)
    level_name = Required(str, unique=True, max_len=20)  # 'low', 'medium', 'high'
    description = Optional(str)

    # Связи
    crops = Set('Crop')


class Crop(db.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, max_len=100)
    latin_name = Optional(str, max_len=100)
    family = Required(PlantFamily)
    appetite_level = Required(AppetiteLevel)

    # Агрономические характеристики
    crop_type = Optional(str, max_len=50)  # 'grain', 'vegetable', 'legume', 'root', 'technical'
    nutrient_demand = Optional(str, max_len=20)  # 'low', 'medium', 'high'
    water_demand = Optional(str, max_len=20)  # 'low', 'medium', 'high'
    disease_risk = Optional(str, max_len=20)  # 'low', 'medium', 'high'
    preferred_ph = Optional(str, max_len=20)  # 'acidic', 'neutral', 'alkaline'
    recommended_rotation_interval = Required(int, default=3)  # Минимальный интервал в годах

    created_at = Required(datetime, default=datetime.utcnow)

    # Связи
    plantings = Set('Planting')
    rotation_rules_as_previous = Set('CropRotationRule', reverse='previous_crop')
    rotation_rules_as_next = Set('CropRotationRule', reverse='next_crop')
    rotation_recommendations = Set('RotationRecommendation')


class CropRotationRule(db.Entity):
    id = PrimaryKey(int, auto=True)
    previous_crop = Required(Crop, reverse='rotation_rules_as_previous')
    next_crop = Required(Crop, reverse='rotation_rules_as_next')
    compatibility = Required(str, max_len=20)  # 'good', 'neutral', 'bad'
    rule_description = Optional(str)
    created_at = Required(datetime, default=datetime.utcnow)


class Planting(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)
    crop = Required(Crop)
    season = Required(Season)

    # Детали посадки
    planting_date = Required(datetime)
    harvest_date = Optional(datetime)
    yield_amount = Optional(float)  # Урожайность в т/га
    yield_quality = Optional(str, max_len=20)  # 'poor', 'fair', 'good', 'excellent'
    notes = Optional(str)

    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Required(datetime, default=datetime.utcnow)


class FieldSoilProfile(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)

    # Химические показатели
    pH = Optional(float)
    organic_matter = Optional(float)  # %
    nitrogen = Optional(float)  # мг/кг
    phosphorus = Optional(float)  # мг/кг
    potassium = Optional(float)  # мг/кг
    nutrient_level = Optional(Json)  # Дополнительные показатели

    # Физические показатели
    moisture_content = Optional(float)  # %
    soil_density = Optional(float)  # г/см³

    sample_date = Required(datetime)
    created_at = Required(datetime, default=datetime.utcnow)


class FieldObservation(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)
    date = Required(datetime)
    pest_pressure = Optional(int)  # 1-5 шкала
    disease_signs = Optional(str)
    weed_pressure = Optional(int)  # 1-5 шкала
    crop_condition = Optional(str, max_len=20)  # 'poor', 'fair', 'good', 'excellent'
    yield_estimate = Optional(float)
    notes = Optional(str)

    created_at = Required(datetime, default=datetime.utcnow)


class IrrigationRecord(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)
    operator = Optional(User)
    date = Required(datetime)
    amount_mm = Optional(float)
    method = Optional(str, max_len=50)  # 'drip', 'sprinkler', 'flood'
    water_source = Optional(str, max_len=50)
    notes = Optional(str)

    created_at = Required(datetime, default=datetime.utcnow)


class InputsLog(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)
    date = Required(datetime)
    product = Required(str, max_len=100)
    product_type = Optional(str, max_len=50)  # 'fertilizer', 'pesticide', 'herbicide', 'fungicide'
    amount = Required(float)
    unit = Required(str, max_len=20)
    supplier = Optional(str, max_len=100)
    application_method = Optional(str, max_len=50)
    notes = Optional(str)

    created_at = Required(datetime, default=datetime.utcnow)


class RotationRecommendation(db.Entity):
    id = PrimaryKey(int, auto=True)
    field = Required(Field)
    crop = Required(Crop)
    target_year = Required(int)

    # Оценки
    agro_score = Required(int)  # 0-100
    compatibility = Required(str, max_len=20)  # 'excellent', 'good', 'fair', 'poor'

    # Причины рекомендации
    reasons = Optional(Json)  # Список причин в формате JSON
    soil_adaptation = Required(bool, default=False)
    rotation_compliance = Required(bool, default=False)

    generated_at = Required(datetime, default=datetime.utcnow)
    is_applied = Required(bool, default=False)

