import pytest
from starlette.testclient import TestClient

from app.main import app

@pytest.fixture(scope="module")
def test_app():
    client = TestClient(app)
    yield client

@pytest.mark.asyncio
async def test_index(test_app):
    response = test_app.get('/')
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}