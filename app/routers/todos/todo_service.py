from typing import List
from app.routers.todos.todo_interface import ITodo
from app.routers.todos.todo_model import Todo


class TodoService(ITodo):

    @staticmethod
    async def add_todos(todo_list: List[dict]) -> List[Todo]:
        todos = [Todo(**todo) for todo in todo_list]
        try:
            await Todo.insert_many(todos)
            return todos
        except Exception as e:
            return e
        
    @staticmethod
    async def get_all_todos() -> List[Todo]:
        return await Todo.find_all().to_list()
    
    @staticmethod
    async def get_specific_todos(skip: int, limit: int) -> List[Todo]:
        return await Todo.find(skip=skip, limit=limit).to_list()
    
    @staticmethod
    async def get_todo_by_id(todo_id: int) -> Todo:
        todo = await Todo.find_one(Todo.id == todo_id)
        if not todo:
            return None
        return todo