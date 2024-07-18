from typing import List, Optional
from app.routers.todos.todo_interface import ITodo
from app.routers.todos.todo_model import Todo


class TodoService(ITodo):

    @staticmethod
    async def add_todos(todo_list: List[dict]) -> List[Todo]:
        """
            Inserts a list of todos to the database.

            Args:
                todo_list (List[dict]): Gets a list of todos

            Returns:
                Todos based on the Todo Model
        """
        todos = [Todo(**todo) for todo in todo_list]
        try:
            await Todo.insert_many(todos)
            return todos
        except Exception as e:
            return e
        
    @staticmethod
    async def get_all_todos() -> List[Todo]:
        """
            Get all the todos

            Returns:
                A list of todos
        """
        return await Todo.find_all().to_list()
    
    @staticmethod
    async def get_specific_todos(skip: int, limit: int) -> List[Todo]:
        """
            Get a limited list of todos

            Args:
                skip (int): The number of todos to skip
                limit (int): Maximum number of todos to obtain

            Returns:
                A list of todos based on the Todo Model
        """
        return await Todo.find(skip=skip, limit=limit).to_list()
    
    @staticmethod
    async def get_todo_by_id(todo_id: int) -> Optional[Todo]:
        """
            Get comment by the id

            Args:
                comment_id (int): The id of the comment to get

            Returns:
                comment based on the Comment Model or None
        """
        todo = await Todo.find_one(Todo.id == todo_id)
        if not todo:
            return None
        return todo