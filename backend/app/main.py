from fastapi import FastAPI
from backend.auth.router import router as auth_router
from backend.db.database import db
from backend.db import models
from backend.crops.router import router as crops_router
from backend.fields.router import router as fields_router
from backend.groups.router import router as groups_router

db.bind(provider="postgres", user="...", password="...", host="...", database="...")
db.generate_mapping(create_tables=True)

app = FastAPI(title="Agro App")
app.include_router(auth_router)
app.include_router(fields_router)
app.include_router(crops_router)
app.include_router(groups_router)






