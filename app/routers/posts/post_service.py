from typing import List
from app.routers.posts.post_interface import IPost
from app.routers.posts.post_model import Post
from app.routers.users.user_model import User


class PostService(IPost):

    @staticmethod
    async def get_all_posts() -> List[Post]:
        posts = await Post.find_all().to_list()
        return posts
    
    @staticmethod
    async def get_post(id: int) -> Post:
        post = await Post.find_one(Post.id == id)
        if not post:
            return None
        return post
    
    @staticmethod
    async def get_specific_posts(skip: int, limit: int) -> List[Post]:
        return await Post.find(skip=skip, limit=limit).to_list()

    @staticmethod
    async def add_posts(post_list: List[dict]) -> List[Post]:
        posts = []
        for post in post_list:
            post_in = Post(**post)
            posts.append(post_in)
        try:
            await Post.insert_many(posts)
            return posts
        except:
            return None
        