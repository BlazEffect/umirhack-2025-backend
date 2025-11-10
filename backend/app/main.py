from fastapi import FastAPI
from auth.router import router as auth_router
from auth.models import db
from backend.db.database import db
from backend.db import models
from backend.fields.router import router as fields_router
from config import settings

db.bind(provider="postgres", user="...", password="...", host="...", database="...")
db.generate_mapping(create_tables=True)

app = FastAPI(title="Agro App")
app.include_router(auth_router)
app.include_router(fields_router)

