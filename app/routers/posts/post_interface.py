from abc import ABC, abstractmethod
from typing import List

from app.routers.posts.post_model import Post
from app.routers.posts.post_schema import PostCreate


class IPost(ABC):

    @staticmethod
    @abstractmethod
    async def add_posts(post_list: List[Post]):

        pass