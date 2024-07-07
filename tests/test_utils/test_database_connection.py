from unittest.mock import AsyncMock, MagicMock, patch
import pytest
from app.utils.database_connection import DatabaseConnection

class TestDatabaseConnection:

    @pytest.mark.asyncio
    @patch('app.utils.database_connection.AsyncIOMotorClient')
    async def test_ping_server(self, MockAsyncIOMotorClient):

        mock_client = MockAsyncIOMotorClient.return_value
        mock_client.admin.command = AsyncMock()

        connection = DatabaseConnection()

        await connection.ping_server()

        mock_client.admin.command.assert_awaited_with('ping')

    @pytest.mark.asyncio
    @patch('app.utils.database_connection.AsyncIOMotorClient')
    async def test_get_database(self, MockAsyncIOMotorClient):

        mock_client = MockAsyncIOMotorClient.return_value
        mock_database = MagicMock()
        mock_client.__getitem__.return_value = mock_database

        connection = DatabaseConnection()

        db = await connection.get_database()

        db == mock_database

    @pytest.mark.asyncio
    @patch('app.utils.database_connection.AsyncIOMotorClient')
    async def test_close(self, MockAsyncIOMotorClient):

        mock_client = MockAsyncIOMotorClient.return_value

        connection = DatabaseConnection()

        await connection.close()

        mock_client.close.assert_called_once()