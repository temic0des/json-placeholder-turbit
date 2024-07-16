from typing import List

from app.routers.albums.album_model import Album
from app.routers.posts.post_model import Post
from app.routers.users.user_interface import IUser
from app.routers.users.user_model import User
from app.routers.users.user_schema import UserCreate, UserPostRead, UserRead, UserUpdate
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
    async def get_all_users() -> List[UserRead]:
        users = await User.find_all().to_list()
        user_data = []
        for user in users:
            post_count = await Post.find(Post.user_id == user.id).count()
            user_read = UserRead(**user.model_dump(), number_of_posts=post_count)
            user_data.append(user_read)
        return user_data
    
    @staticmethod
    async def get_user(id: int) -> UserRead:
        user = await User.find_one(User.id == id)
        if not user:
            return None
        post_count = await Post.find(Post.user_id == id).count()
        user_dict = UserRead(**user.model_dump(), number_of_posts=post_count)
        return user_dict
    
    @staticmethod
    async def add_users(user_list: list[dict]) -> List[User]:   
        users = [User(**user) for user in user_list]
        try:
            await User.insert_many(users)
            return users
        except Exception as e:
            return e
 
        
    @staticmethod
    async def get_user_posts(id: int) -> UserPostRead:
        user = await User.find_one(User.id == id)
        if not user:
            return None
        user_posts = await Post.find(Post.user_id == id).to_list()
        user_data_read = UserPostRead(**user.model_dump(), posts=user_posts)
        return user_data_read

    @staticmethod
    async def get_specific_users(skip: int, limit: int) -> List[UserRead]:
        users = await User.find(skip=skip, limit=limit).to_list()
        user_data = []
        for user in users:
            post_count = await Post.find(Post.user_id == user.id).count()
            user_read = UserRead(**user.model_dump(), number_of_posts=post_count)
            user_data.append(user_read)
        return user_data