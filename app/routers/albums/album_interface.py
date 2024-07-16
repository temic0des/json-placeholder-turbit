from abc import ABC, abstractmethod
from typing import List

from app.routers.albums.album_model import Album
from app.routers.albums.album_schema import AlbumCreate


class IAlbum(ABC):

    @staticmethod
    @abstractmethod
    async def add_albums(album_list: List[dict]) -> List[Album]:
        pass

    @staticmethod
    @abstractmethod
    async def get_all_albums() -> List[Album]:
        pass

    @staticmethod
    @abstractmethod
    async def get_specific_albums(skip: int, limit: int) -> List[Album]:
        pass

    @staticmethod
    @abstractmethod
    async def get_album_by_id(album_id: int) -> Album:
        pass