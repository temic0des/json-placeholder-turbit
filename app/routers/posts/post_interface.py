from abc import ABC, abstractmethod
from typing import List

from app.routers.posts.post_model import Post
from app.routers.posts.post_schema import PostCreate


class IPost(ABC):

    @staticmethod
    @abstractmethod
    async def add_posts(post_list: List[Post]):
        pass

    @staticmethod
    @abstractmethod
    async def get_all_posts() -> List[Post]:
        pass

    @staticmethod
    @abstractmethod
    async def get_specific_posts(skip: int, limit: int) -> List[Post]:
        pass