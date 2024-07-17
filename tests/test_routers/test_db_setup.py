from beanie import init_beanie
import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from app.routers.users.user_model import User
from app.utils.document_models import document_models
from tests.test_routers.test_users.data_dump import user_data

@pytest.mark.asyncio(scope='module')
async def setup_database():
    client = AsyncIOMotorClient("mongodb://localhost:27017", uuidRepresentation='standard')
    db = client["test_db"]
    await init_beanie(database=db, document_models=document_models)
    yield
    client.drop_database("test_db")