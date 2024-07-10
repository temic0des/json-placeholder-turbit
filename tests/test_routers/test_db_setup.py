from beanie import init_beanie
import pytest
from motor.motor_asyncio import AsyncIOMotorClient

from app.common.models.counter_model import Counter
from app.routers.users.user_model import User

@pytest.mark.asyncio(scope='module')
async def setup_database():
    client = AsyncIOMotorClient("mongodb://root:Ankithacker101@localhost:27018", uuidRepresentation='standard')
    db = client["test_db"]
    await init_beanie(database=db, document_models=[User, Counter])
    yield
    client.drop_database("test_db")