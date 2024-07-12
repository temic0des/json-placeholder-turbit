from abc import ABC, abstractmethod
from typing import List

from app.routers.users.user_model import User
from app.routers.users.user_schema import UserCreate, UserRead, UserUpdate

class IUser(ABC):

    @staticmethod
    @abstractmethod
    async def create_user(user_create: UserCreate) -> UserCreate:
        pass

    @staticmethod
    @abstractmethod
    async def update_user(user_update: UserUpdate) -> User:
        pass

    @staticmethod
    @abstractmethod
    async def delete_user(id: int) -> None:
        pass

    @staticmethod
    @abstractmethod
    async def add_users(user_list: list[dict]) -> List[User]:
        pass

    @staticmethod
    @abstractmethod
    async def get_all_users() -> List[UserRead]:
        pass