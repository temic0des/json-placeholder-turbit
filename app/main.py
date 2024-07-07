from contextlib import asynccontextmanager
from beanie import init_beanie
from fastapi import FastAPI
from app.utils.database_connection import db

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
    await init_beanie(database=database_instance, document_models=[])
    yield

app = FastAPI(lifespan=init_db)

@app.get('/')
async def index():
    return {"hello": "world"}