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
        """
            Creates a new user.

            Args:
                user_create (UserCreate): The user information to create.

            Returns:
                UserCreate: The created user
        """

        # Get the name of the collection
        collection_name = User.get_collection_name()

        # Get the next id of the collection
        next_id = await get_next_id(col_name=collection_name)

        # Pass the user information to create into the model
        user_in = User(id=next_id, **user_create.model_dump())

        # Insert to the database
        await user_in.insert()
        return user_create

    @staticmethod
    async def update_user(user_update: UserUpdate, user_id: int) -> User:
        """
            Updates a new user.

            Args:
                user_update (UserUpdate): The information to update the user
                user_id (int): The id of the user to update

            Returns:
                User: The updated user
        """

        # Get user by id
        user = await User.get_user_by_id(id=user_id)

        # Check if the user is None
        if not user:
            return None
        
        # Update the user
        updated_user = await user.set(user_update.model_dump(exclude_unset=True))
        if not updated_user:
            return None
        return user

    @staticmethod
    async def delete_user(user_id: int) -> Optional[User]:
        """
            Deletes a user

            Args:
                user_id (int): The id of the user to delete

            Returns:
                The deleted user
        """

        # Get the user by the id
        user = await User.get_user_by_id(id=user_id)
        if not user:
            return None
        # Deletes the user
        await user.delete()
        return user
    
    @staticmethod
    async def get_all_users() -> List[UserRead]:
        """
            Gets all the users.

            Returns:
                A list of the UserRead schema data 
                with the number of posts for each user
        """

        # Get all the users
        users = await User.find_all().to_list()

        # Create an empty list
        user_data = []
        # Loop through the users
        for user in users:
            # Get the count of each users post
            post_count = await Post.find(Post.user_id == user.id).count()
            # Add the post count to the User Read schema
            user_read = UserRead(**user.model_dump(), number_of_posts=post_count)
            # Append to the user_data list
            user_data.append(user_read)
        return user_data
    
    @staticmethod
    async def get_user(user_id: int) -> UserRead:
        """
            Gets a user.

            Args:
                user_id (int): The id of the user

            Returns:
                A UserRead schema inclusive of the 
                number of posts for each user
        """

        # Get the user by the id
        user = await User.get_user_by_id(id=user_id)
        if not user:
            return None
        # Get the count of each users post
        post_count = await Post.find(Post.user_id == user_id).count()
        # Add the post count to the UserRead schema
        user_data = UserRead(**user.model_dump(), number_of_posts=post_count)
        return user_data
    
    @staticmethod
    async def add_users(user_list: list[dict]) -> List[User]:
        """
            Send a list of users to the database
        """   
        users = [User(**user) for user in user_list]
        try:
            # Insert many users
            await User.insert_many(users)
            return users
        except Exception as e:
            return e
 
        
    @staticmethod
    async def get_user_posts(user_id: int) -> UserPostRead:
        """
            Gets a user and the posts created by the user

            Args:
                user_id (int): The id of the user

            Returns:
                A user and a list of posts for the user
        """

        # Get the user by id
        user = await User.get_user_by_id(id=user_id)
        if not user:
            return None
        # Get the posts associated with the user
        user_posts = await Post.find(Post.user_id == user_id).to_list()

        # Empty list for the post
        posts_read = []
        # Loop through each users post
        for user_post in user_posts:
            # Get each comments count
            comment_count = await Comment.find(Comment.post_id == user_post.id).count()
            # Append the users posts and comment count to the list
            posts_read.append(PostRead(**user_post.model_dump(), number_of_comments=comment_count))
        user_post_read = UserPostRead(**user.model_dump(), posts=posts_read)
        return user_post_read
    
    @staticmethod
    async def get_user_albums(user_id: int) -> UserAlbumRead:
        """
            Gets a user and the albums created by the user

            Args:
                user_id (int): The id of the user

            Returns:
                A user and a list of albums for the user
        """

        # Get the user by id
        user = await User.get_user_by_id(id=user_id)
        if not user:
            return None
        # Get the albums associated with the user
        user_albums = await Album.find(Album.user_id == user_id).to_list()
        # Attach each album to the AlbumRead schema
        albums_read = [AlbumRead(**user_album.model_dump()) for user_album in user_albums]
        # UserAlbumRead user model with the list of albums
        user_album_read = UserAlbumRead(**user.model_dump(), albums=albums_read)
        return user_album_read

    @staticmethod
    async def get_specific_users(skip: int, limit: int) -> List[UserRead]:
        """
            Get a subset of users

            Args:
                skip (int): The number of users to skip
                limit (int): Maximum number of users to obtain

            Returns:
                A list of users with the UserRead schema
        """

        # Get a list of users from a starting point 
        # to the limit of the number of users to get
        users = await User.find(skip=skip, limit=limit).to_list()
        user_data = []
        for user in users:
            # Get the count of the posts for each user
            post_count = await Post.find(Post.user_id == user.id).count()
            # Get an instance of each UserRead schema with the number of posts
            user_read = UserRead(**user.model_dump(), number_of_posts=post_count)
            # Append to the user_data
            user_data.append(user_read)
        return user_data