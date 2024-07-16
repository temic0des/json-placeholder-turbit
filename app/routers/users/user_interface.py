from abc import ABC, abstractmethod
from typing import List

from app.routers.users.user_model import User
from app.routers.users.user_schema import UserAlbumRead, UserCreate, UserPostRead, UserRead, UserUpdate

class IUser(ABC):

    @staticmethod
    @abstractmethod
    async def create_user(user_create: UserCreate) -> UserCreate:
        pass

    @staticmethod
    @abstractmethod
    async def update_user(user_update: UserUpdate, user_id: int) -> User:
        pass

    @staticmethod
    @abstractmethod
    async def delete_user(user_id: int) -> None:
        pass

    @staticmethod
    @abstractmethod
    async def add_users(user_list: list[dict]) -> List[User]:
        pass

    @staticmethod
    @abstractmethod
    async def get_all_users() -> List[UserRead]:
        pass

    @staticmethod
    @abstractmethod
    async def get_user_posts(user_id: int) -> UserPostRead:
        pass

    @staticmethod
    @abstractmethod
    async def get_user_albums(user_id: int) -> UserAlbumRead:
        pass

    @staticmethod
    @abstractmethod
    async def get_specific_users(skip: int, limit: int) -> List[UserRead]:
        pass