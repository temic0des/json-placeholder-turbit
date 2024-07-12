from contextlib import asynccontextmanager
from beanie import init_beanie
from fastapi import FastAPI
from app.routers.router import router
from app.utils.api_urls import run_seed
from app.utils.database_connection import db
from app.utils.document_models import document_models
from app.utils.settings import settings
from app.utils.functions import initialize_counter

@asynccontextmanager
async def init_db(_: FastAPI):
    """
    Initializes the database by calling the `init_beanie` function with the appropriate parameters.
    
    Parameters:
        _: FastAPI: The FastAPI instance.
    
    Yields:
        None
    """
    await db.ping_server()
    database_instance = await db.get_database()
    # Beanie Initialization
    await init_beanie(database=database_instance, document_models=document_models)
    # Seed Run
    await run_seed()
    # Counter Initialization
    await initialize_counter(models=document_models)
    yield

app = FastAPI(lifespan=init_db, title=settings.app_name)

@app.get('/')
async def index():
    return {"hello": "world"}

app.include_router(router=router)