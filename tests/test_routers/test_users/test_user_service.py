from app.routers.users.user_schema import UserCreate
from app.routers.users.user_service import UserService
from tests.test_routers.test_users.data_dump import user_data
import pytest
import pytest_asyncio
from app.routers.users.user_model import User
from tests.test_routers.test_users.data_dump import user_data
from tests.test_routers.test_db_setup import setup_database

@pytest.fixture
async def test_user(setup_database):
    user = User(**user_data[0])
    await user.insert()
    return user

class TestUserService:

    @pytest_asyncio.fixture(autouse=True)
    async def setup_class(self, setup_database, user_service: UserService):
        self.database = setup_database
        self.user_service = user_service

    @pytest.mark.asyncio
    async def test_add_users(self):
        users = []
        for user in user_data:
            user_in = User(**user)
            users.append(user_in)

        result = await self.user_service.add_users(user_list=user_data)
        assert result == users

        documents = await User.find_all().to_list()
        assert len(documents) == len(user_data)
        for index, document in enumerate(documents):
            assert document.name == user_data[index]["name"]
            assert document.email == user_data[index]["email"]

    @pytest.mark.asyncio
    async def test_create_user(self):
        data = {
            "id": 1,
            "name": "John Snow",
            "username": "John",
            "email": "Johnsnow@april.biz",
            "address": {
                "street": "Main Street",
                "suite": "Apt. 556",
                "city": "London",
                "zipcode": "47853-7834",
                "geo": {"lat": "-37.3159", "lng": "81.1496"},
            },
            "phone": "1-894-453-4902 x56442",
            "website": "hildegard.org",
            "company": {
                "name": "Romaguera-Crona",
                "catchPhrase": "Multi-layered client-server neural-net",
                "bs": "harness real-time e-markets",
            },
        }
        user_create = UserCreate(**data)
        new_user = await self.user_service.create_user(user_create=user_create)
        assert new_user.email == user_create.email
        assert new_user.email == data.get('email')
        assert new_user.name == user_create.name
        assert new_user.name == data.get('name')

        document = await User.find_one(User.email == user_create.email)
        assert document.email == user_create.email
        assert document.address.street == user_create.address.street
        assert document.address.street == data.get('address')['street']


    @pytest.mark.asyncio
    async def test_get_user(self, test_user):
        user = await self.user_service.get_user(user_id=test_user)
        assert user is not None
        assert user.username == "Bret"