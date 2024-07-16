from typing import List
from app.routers.comments.comment_model import Comment
from app.routers.posts.post_interface import IPost
from app.routers.posts.post_model import Post
from app.routers.posts.post_schema import PostCommentRead, PostRead


class PostService(IPost):

    @staticmethod
    async def get_all_posts() -> List[PostRead]:
        posts = await Post.find_all().to_list()
        post_data = []
        for post in posts:
            comment_count = await Comment.find(Comment.post_id == post.id).count()
            post_read = PostRead(**post.model_dump(), number_of_comments=comment_count)
            post_data.append(post_read)
        return post_data
    
    @staticmethod
    async def get_post(id: int) -> PostRead:
        post = await Post.find_one(Post.id == id)
        if not post:
            return None
        comment_count = await Comment.find(Comment.post_id == id).count()
        post_read = PostRead(**post.model_dump(), number_of_comments=comment_count)
        return post_read
    
    @staticmethod
    async def get_specific_posts(skip: int, limit: int) -> List[PostRead]:
        posts = await Post.find(skip=skip, limit=limit).to_list()
        post_data = []
        for post in posts:
            comment_count = await Comment.find(Comment.post_id == post.id).count()
            post_read = PostRead(**post.model_dump(), number_of_comments=comment_count)
            post_data.append(post_read)
        return post_data

    @staticmethod
    async def add_posts(post_list: List[dict]) -> List[Post]:
        posts = [Post(**post) for post in post_list]
        try:
            await Post.insert_many(posts)
            return posts
        except Exception as e:
            return e
        
    
    @staticmethod
    async def get_comments_by_post(id: int) -> PostCommentRead:
        post = await Post.find_one(Post.id == id)
        if not post:
            return None
        comments = await Comment.find(Comment.post_id == id).to_list()
        post_comments = PostCommentRead(**post.model_dump(), comments=comments)
        return post_comments