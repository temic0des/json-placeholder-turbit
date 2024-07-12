from contextlib import asynccontextmanager
from beanie import init_beanie
from fastapi import FastAPI
from app.routers.router import router
from app.common.seed_data.seed_data import SeedData
from app.utils.api_urls import API_URLS
from app.utils.database_connection import db
from app.utils.document_models import document_models
from app.utils.functions import initialize_counter
from app.utils.settings import settings

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
    # User Seed
    user_seed = SeedData(url=API_URLS.get('user_url'))
    await user_seed.user_seed()
    post_seed = SeedData(url=API_URLS.get('post_url'))
    await post_seed.post_seed()
    await initialize_counter(models=document_models)
    yield

app = FastAPI(lifespan=init_db, title=settings.app_name)

@app.get('/')
async def index():
    return {"hello": "world"}

app.include_router(router=router)