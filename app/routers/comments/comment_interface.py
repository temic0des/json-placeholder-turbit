from abc import ABC, abstractmethod
from typing import List
from app.routers.comments.comment_model import Comment


class IComment(ABC):

    @staticmethod
    @abstractmethod
    async def add_comments(comment_list: List[dict]) -> List[Comment]:
        pass

    @staticmethod
    @abstractmethod
    async def get_all_comments() -> List[Comment]:
        pass

    @staticmethod
    @abstractmethod
    async def get_comment_by_id(comment_id: int) -> Comment:
        pass

    @staticmethod
    @abstractmethod
    async def get_specific_comments() -> List[Comment]:
        pass