from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.common.schemas.response_model import ResponseModel
from app.routers.users.user_schema import UserCreate, UserPostRead, UserRead, UserUpdate
from app.routers.users.user_service import UserService
from pymongo.errors import DuplicateKeyError, PyMongoError

from app.security.dependencies import get_user_service 

class UserEndpoint:

    def __init__(self) -> None:
        self.user_router = APIRouter(tags=['Users'], prefix='/users')
        self.register_user_routes()

    def register_user_routes(self):
        self.user_router.post('', response_model=ResponseModel, 
                              status_code=status.HTTP_201_CREATED)(self.create_user)
        self.user_router.get('/all', response_model=List[UserRead])(self.get_all_users)
        self.user_router.get('/{id}', response_model=UserRead)(self.get_user)
        self.user_router.get('/{id}/posts', response_model=UserPostRead)(self.get_user_posts)
        self.user_router.patch('/{id}', response_model=ResponseModel)(self.update_user)
        self.user_router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)(self.delete_user)
        self.user_router.get('', response_model=List[UserRead])(self.get_limited_users)
        

    async def create_user(self, user_create: UserCreate, user_service: UserService = Depends(get_user_service)) -> ResponseModel:
        try:
            new_user = await user_service.create_user(user_create=user_create)
            return ResponseModel(message="User Successfully Created", success=True, data=new_user.email)
        except DuplicateKeyError as dke:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{dke.details}')
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
    
    
    async def update_user(self, id: int, user_update: UserUpdate = Body(...), user_service: UserService = Depends(get_user_service)) -> ResponseModel:
        try:
            updated_user = await user_service.update_user(user_update=user_update, id=id)
            if not updated_user:
                raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)
            return ResponseModel(message="User Updated Successfully", success=True, data=updated_user)
        except DuplicateKeyError as dke:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{dke.details}')
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def delete_user(self, id: int, user_service: UserService = Depends(get_user_service)):
        try:
            deleted_user = await user_service.delete_user(id=id)
            if not deleted_user:
                raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)
            return ResponseModel(message=f"{deleted_user.email} deleted", success=True)
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')

    async def get_all_users(self, user_service: UserService = Depends(get_user_service)) -> List[UserRead]:
        try:
            user_data = await user_service.get_all_users()
            return user_data
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
        
    async def get_user(self, id: int, user_service: UserService = Depends(get_user_service)) -> UserRead:
        try:
            user_data = await user_service.get_user(id=id)
            if not user_data:
                raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
            return user_data
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def get_user_posts(self, id: int, user_service: UserService = Depends(get_user_service)) -> UserPostRead:
        try:
            user_posts = await user_service.get_user_posts(id=id)
            if not user_posts:
                raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
            return user_posts
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        

    async def get_limited_users(self, skip: int = 0, limit: int = 10, user_service: UserService = Depends(get_user_service)) -> List[UserRead]:
        try:
            user_data = await user_service.get_specific_users(skip=skip, limit=limit)
            return user_data
        except PyMongoError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')