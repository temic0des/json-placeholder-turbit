from app.utils.settings import settings
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class DatabaseConnection:

    _MONGO_URL = settings.mongo_url
    _DATABASE_NAME = settings.mongo_initdb_root_dbname

    def __init__(self) -> None:
        mongo_url = str(self._MONGO_URL)
        self._client = AsyncIOMotorClient(mongo_url, uuidRepresentation='standard')
        self._db = self._client[self._DATABASE_NAME]

    async def ping_server(self):
        try:
            await self._client.admin.command('ping')
            print('Successfully connected to MongoDB!')
        except Exception as e:
            print(e)

    async def get_database(self) -> AsyncIOMotorDatabase:
        db_instance = self._db
        return db_instance

    async def close(self):
        self._client.close()

db = DatabaseConnection()