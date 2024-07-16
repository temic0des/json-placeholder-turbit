from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import PyMongoError

from app.routers.todos.todo_schema import TodoRead
from app.routers.todos.todo_service import TodoService
from app.security.dependencies import get_todo_service


class TodoEndpoint:

    def __init__(self) -> None:
        self.todo_router = APIRouter(tags=['Todos'], prefix='/todos')
        self.register_todo_routes()

    def register_todo_routes(self):
        self.todo_router.get('/all', response_model=List[TodoRead])(self.fetch_all_todos)
        self.todo_router.get('', response_model=List[TodoRead])(self.fetch_limited_todos)
        self.todo_router.get('/{todo_id}', response_model=TodoRead)(self.fetch_todo_by_id)

    async def fetch_all_todos(self, todo_service: TodoService = Depends(get_todo_service)):
        try:
            return await todo_service.get_all_todos()
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_limited_todos(self, skip: int = 0, limit: int = 10, todo_service: TodoService = Depends(get_todo_service)):
        try:
            return await todo_service.get_specific_todos(skip=skip, limit=limit)
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_todo_by_id(self, todo_id: int, todo_service: TodoService = Depends(get_todo_service)):
        try:
            todo = await todo_service.get_todo_by_id(todo_id=todo_id)
            if not todo:
                raise HTTPException(detail="Todo not found", status_code=status.HTTP_404_NOT_FOUND)
            return todo
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        