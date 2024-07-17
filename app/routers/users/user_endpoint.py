from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status

from app.common.schemas.response_model import ResponseModel
from app.routers.users.user_schema import UserAlbumRead, UserCreate, UserPostRead, UserRead, UserTodoRead, UserUpdate
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
        self.user_router.get('/all', response_model=List[UserRead])(self.fetch_all_users)
        self.user_router.get('/{user_id}', response_model=UserRead)(self.fetch_user)
        self.user_router.get('/{user_id}/posts', response_model=UserPostRead)(self.fetch_user_posts)
        self.user_router.get('/{user_id}/albums', response_model=UserAlbumRead)(self.fetch_user_albums)
        self.user_router.get('/{user_id}/todos', response_model=UserTodoRead)(self.fetch_user_todos)
        self.user_router.patch('/{user_id}', response_model=ResponseModel)(self.update_user)
        self.user_router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)(self.delete_user)
        self.user_router.get('', response_model=List[UserRead])(self.fetch_limited_users)
        

    async def create_user(self, user_create: UserCreate, user_service: UserService = Depends(get_user_service)) -> ResponseModel:
        """
            Create a new user.

            Args:
                user_create (UserCreate): The user information to create.
                user_service (UserService): Defaults to Depends(get_user_service).

            Returns:
                ResponseModel: The response containing the created user information.

            Raises:
                HTTPException: If the user is not found, there are duplicates or internal server error occurs
        """
        try:
            # Gets the create user service
            new_user = await user_service.create_user(user_create=user_create)
            # Returns a ResponseModel with a message and created email
            return ResponseModel(message="User Successfully Created", success=True, data=new_user.email)
        except DuplicateKeyError as dke:
            # Raises an exception if there are duplicates
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{dke.details}')
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catch other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
    
    
    async def update_user(self, user_id: int, user_update: UserUpdate = Body(...), user_service: UserService = Depends(get_user_service)) -> ResponseModel:
        """
            Updates a user.

            Args:
                user_id (int): The id of the user to update.
                user_update (UserUpdate): The user information to update.
                user_service (UserService): Defaults to Depends(get_user_service).

            Returns:
                ResponseModel: The response containing the created user information.

            Raises:
                HTTPException: If the user is not found, there are duplicates or internal server error occurs
        """
        try:
            updated_user = await user_service.update_user(user_update=user_update, user_id=user_id)
            if not updated_user:
                # Raises an exception if the user does not exist
                raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)
            return ResponseModel(message="User Updated Successfully", success=True, data=updated_user)
        except DuplicateKeyError as dke:
            # Raises an exception if there are duplicates
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{dke.details}')
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catch other exceptions in the BaseException class
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def delete_user(self, user_id: int, user_service: UserService = Depends(get_user_service)):
        """
            Deletes a user.

            Args:
                user_id (int): The id of the user to delete.
                user_service (UserService): Defaults to Depends(get_user_service).

            Returns:
                ResponseModel: The response after a user has been deleted.

            Raises:
                HTTPException: If the user is not found, there are duplicates or internal server error occurs
        """
        try:
            deleted_user = await user_service.delete_user(user_id=user_id)
            if not deleted_user:
                # Raises an exception if the user does not exist
                raise HTTPException(detail='User not found', status_code=status.HTTP_404_NOT_FOUND)
            return ResponseModel(message=f"{deleted_user.email} deleted", success=True)
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catch other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')

    async def fetch_all_users(self, user_service: UserService = Depends(get_user_service)) -> List[UserRead]:
        """
            Fetches all the users

            Args:
                user_service (UserService): Defaults to Depends(get_user_service).

            Returns:
                A list of users based on the schema UserRead
        """
        try:
            # Get all the users
            user_data = await user_service.get_all_users()
            return user_data
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catches other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
        
    async def fetch_user(self, user_id: int, user_service: UserService = Depends(get_user_service)) -> UserRead:
        """
            Fetches a user.

            Args:
                user_id (int): The id of the user to get.
                user_service (UserService): Defaults to Depends(get_user_service).

            Returns:
                A user based on the UserRead schema.
        """
        try:
            # Try to get the user
            user_data = await user_service.get_user(user_id=user_id)
            if not user_data:
                # Raises an exception if the user does not exist
                raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
            return user_data
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catches other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_user_posts(self, user_id: int, user_service: UserService = Depends(get_user_service)) -> UserPostRead:
        """
            Fetches the user and the posts created by the user.

            Args:
                user_id (int): The id of the user to get.
                user_service (UserService): Defaults to Depends(get_user_service).

            Returns:
                A user with a list of posts based on the UserPostRead schema.
        """
        try:
            # Try to get the user and their posts
            user_posts = await user_service.get_user_posts(user_id=user_id)
            if not user_posts:
                # Raise an exception of the user does not exist
                raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
            return user_posts
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catches other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_user_albums(self, user_id: int, user_service: UserService = Depends(get_user_service)) -> UserAlbumRead:
        """
            Fetches the user and the user albums.

            Args:
                user_id (int): The id of the user to get.
                user_service (UserService): Defaults to Depends(get_user_service).

            Returns:
                A user with a list of albums based on the UserAlbumRead schema.
        """
        try:
            # Try to get the user and their albums
            user_albums = await user_service.get_user_albums(user_id=user_id)
            if not user_albums:
                # Raise an exception of the user does not exist
                raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
            return user_albums
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catches other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')
        
    async def fetch_user_todos(self, user_id: int, user_service: UserService = Depends(get_user_service)) -> UserTodoRead:
        """
            Fetches the user and the user todos.

            Args:
                user_id (int): The id of the user to get.
                user_service (UserService): Defaults to Depends(get_user_service).

            Returns:
                A user with a list of todos based on the UserTodoRead schema.
        """
        try:
            # Try to get the user and their todos
            user_todos = await user_service.get_user_todos(user_id=user_id)
            if not user_todos:
                # Raise an exception of the user does not exist
                raise HTTPException(detail="User not found", status_code=status.HTTP_404_NOT_FOUND)
            return user_todos
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catches other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')

    async def fetch_limited_users(self, skip: int = 0, limit: int = 10, user_service: UserService = Depends(get_user_service)) -> List[UserRead]:
        """
            Fetches a list of users depending on the number of users to
            skip and the maximum number of users to get

            Args:
                skip (int): The number of users to skip
                limit (int): Maximum number of users to obtain
                user_service (UserService): Defaults to Depends(get_user_service).

            Returns:
                A list of users based on the UserRead schema.
        """
        try:
            # Get the users
            user_data = await user_service.get_specific_users(skip=skip, limit=limit)
            return user_data
        except PyMongoError as e:
            # Raises an exception if an error occurs while interacting with the database
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'{e._message}')
        except Exception as e:
            # Catches other exceptions
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'{e}')