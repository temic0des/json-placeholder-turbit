# conftest.py
import asyncio
from beanie import init_beanie
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.common.models.counter_model import Counter
from app.routers.users.user_model import User
from app.routers.users.user_service import UserService

@pytest_asyncio.fixture
async def setup_database():
    client = AsyncIOMotorClient("mongodb://root:Ankithacker101@localhost:27018", uuidRepresentation='standard')
    db = client["test_db"]
    await init_beanie(database=db, document_models=[User, Counter])
    yield
    client.drop_database("test_db")

@pytest_asyncio.fixture
async def user_service():
    service = UserService()
    yield service