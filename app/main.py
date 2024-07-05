from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def init_db(_: FastAPI):
    yield

app = FastAPI(lifespan=init_db)

@app.get('/')
async def index():
    return {"hello": "world"}