from typing import List, Optional

from app.routers.albums.album_model import Album
from app.routers.albums.album_schema import AlbumRead
from app.routers.comments.comment_model import Comment
from app.routers.posts.post_model import Post
from app.routers.posts.post_schema import PostRead
from app.routers.users.user_interface import IUser
from app.routers.users.user_model import User
from app.routers.users.user_schema import UserAlbumRead, UserCreate, UserPostRead, UserRead, UserUpdate
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
    async def update_user(user_update: UserUpdate, user_id: int) -> User:
        user = await User.get_user_by_id(id=user_id)
        if not user:
            return None
        updated_student = await user.set(user_update.model_dump(exclude_unset=True))
        if not updated_student:
            return None
        return user

    @staticmethod
    async def delete_user(user_id: int) -> Optional[User]:
        user = await User.get_user_by_id(id=user_id)
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
    async def get_user(user_id: int) -> UserRead:
        user = await User.get_user_by_id(id=user_id)
        if not user:
            return None
        post_count = await Post.find(Post.user_id == user_id).count()
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
    async def get_user_posts(user_id: int) -> UserPostRead:
        user = await User.find_one(User.id == user_id)
        if not user:
            return None
        user_posts = await Post.find(Post.user_id == user_id).to_list()
        posts_read = []
        for user_post in user_posts:
            comment_count = await Comment.find(Comment.post_id == user_post.id).count()
            posts_read.append(PostRead(**user_post.model_dump(), number_of_comments=comment_count))
        user_post_read = UserPostRead(**user.model_dump(), posts=posts_read)
        return user_post_read
    
    @staticmethod
    async def get_user_albums(user_id: int) -> UserAlbumRead:
        user = await User.find_one(User.id == user_id)
        if not user:
            return None
        user_albums = await Album.find(Album.user_id == user_id).to_list()
        albums_read = [AlbumRead(**user_album.model_dump()) for user_album in user_albums]
        user_album_read = UserAlbumRead(**user.model_dump(), albums=albums_read)
        return user_album_read

    @staticmethod
    async def get_specific_users(skip: int, limit: int) -> List[UserRead]:
        users = await User.find(skip=skip, limit=limit).to_list()
        user_data = []
        for user in users:
            post_count = await Post.find(Post.user_id == user.id).count()
            user_read = UserRead(**user.model_dump(), number_of_posts=post_count)
            user_data.append(user_read)
        return user_data