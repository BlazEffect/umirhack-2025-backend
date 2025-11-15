from contextlib import asynccontextmanager

from fastapi import FastAPI
from auth.router import router as auth_router
from crops.router import router as crops_router
from db.models import db
from db.seeder import create_detailed_seed_data
from fields.router import router as fields_router
from groups.router import router as groups_router
from seasons.router import router as seasons_router
from recommendations.router import router as recommendations_router
from calculator.router import router as calculator_router

@asynccontextmanager
async def init_db(app: FastAPI):
    db.generate_mapping(create_tables=True)

    create_detailed_seed_data()

    yield
app = FastAPI(title="Agro App", lifespan=init_db)

url_prefix = "/api"

app.include_router(auth_router, prefix=url_prefix)
app.include_router(fields_router, prefix=url_prefix)
app.include_router(crops_router, prefix=url_prefix)
app.include_router(groups_router, prefix=url_prefix)
app.include_router(seasons_router, prefix=url_prefix)
app.include_router(recommendations_router, prefix=url_prefix)
app.include_router(calculator_router, prefix=url_prefix)
