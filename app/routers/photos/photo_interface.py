from abc import ABC, abstractmethod
from typing import List

from app.routers.photos.photo_model import Photo


class IPhoto(ABC):

    @staticmethod
    @abstractmethod
    async def add_photos(photo_list: List[dict]) -> List[Photo]:
        pass

    @staticmethod
    @abstractmethod
    async def get_all_photos() -> List[Photo]:
        pass

    @staticmethod
    @abstractmethod
    async def get_photo(id: int) -> Photo:
        pass

    @staticmethod
    @abstractmethod
    async def get_specific_photos(skip: int, limit: int) -> List[Photo]:
        pass