from typing import List
from app.routers.posts.post_interface import IPost
from app.routers.posts.post_model import Post


class PostService(IPost):

    @staticmethod
    async def add_posts(post_list: List[Post]) -> List[Post]:
        posts = []
        if len(post_list) > 0:
            for post in post_list:
                post_in = Post(**post)
                posts.append(post_in)
            try:
                await Post.insert_many(posts)
                return posts
            except:
                return None
        else:
            return None