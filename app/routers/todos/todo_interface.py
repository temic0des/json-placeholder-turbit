from abc import ABC, abstractmethod
from typing import List

from app.routers.todos.todo_model import Todo


class ITodo(ABC):

    @staticmethod
    @abstractmethod
    async def add_todos(todo_list: List[dict]) -> List[Todo]:
        pass

    @staticmethod
    @abstractmethod
    async def get_all_todos() -> List[Todo]:
        pass 

    @staticmethod
    @abstractmethod
    async def get_todo_by_id(id: int) -> Todo:
        pass

    @staticmethod
    @abstractmethod
    async def get_specific_todos(skip: int, limit: int) -> List[Todo]:
        pass