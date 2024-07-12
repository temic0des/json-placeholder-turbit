from typing import List

from app.routers.posts.post_model import Post
from app.routers.users.user_interface import IUser
from app.routers.users.user_model import User
from app.routers.users.user_schema import UserCreate, UserDict, UserUpdate
from app.utils.functions import get_next_id

class UserService(IUser):

    @staticmethod
    async def create_user(user_create: UserCreate) -> UserCreate:
        collection_name = User.get_collection_name()
        next_id = await get_next_id(col_name=collection_name)
        user_in = User(id=next_id, **user_create.model_dump())
        await user_in.insert()
        return user_create

    @staticmethod
    async def update_user(user_update: UserUpdate, id: int) -> User:
        user = await User.get_user_by_id(id=id)
        if not user:
            return None
        updated_student = await user.set(user_update.model_dump(exclude_unset=True))
        if not updated_student:
            return None
        return user

    @staticmethod
    async def delete_user(id: int) -> User | None:
        user = await User.get_user_by_id(id=id)
        if not user:
            return None
        await user.delete()
        return user
    
    @staticmethod
    async def get_all_users() -> List[User]:
        users = await User.find_all().to_list()
        return users
    
    @staticmethod
    async def get_user(id: int) -> UserDict:
        user = await User.find_one(User.id == id)
        if not user:
            return None
        post_count = await Post.find(Post.user_id == id).count()
        user_dict = UserDict(user=User(**user.model_dump()), post_count=post_count)
        return user_dict
    
    @staticmethod
    async def add_users(user_list: list[dict]) -> List[User]:
        
        users = []
        for user in user_list:
            user_in = User(**user)
            users.append(user_in)
        try:
            await User.insert_many(users)
            return users
        except Exception as e:
            return None
       