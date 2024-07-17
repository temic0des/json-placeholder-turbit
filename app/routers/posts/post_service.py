from typing import List
from app.routers.comments.comment_model import Comment
from app.routers.posts.post_interface import IPost
from app.routers.posts.post_model import Post
from app.routers.posts.post_schema import PostCommentRead, PostRead


class PostService(IPost):

    @staticmethod
    async def get_all_posts() -> List[PostRead]:
        """
            Gets all the posts

            Returns:
                A list of posts with the comment count for each post
                This is returned based on the PostRead schema.
        """

        # Get all posts
        posts = await Post.find_all().to_list()
        post_data = []
        # Loop through each post
        for post in posts:
            # Get the comment count for each post by the post id
            comment_count = await Comment.find(Comment.post_id == post.id).count()
            # Add the comment count to the post model based on the PostRead schema
            post_read = PostRead(**post.model_dump(), number_of_comments=comment_count)
            # Append to the post_data list
            post_data.append(post_read)
        return post_data
    
    @staticmethod
    async def get_post_by_id(post_id: int) -> PostRead:
        """
            Gets a post by its id

            Args:
                post_id (int): The id of the post to get

            Returns:
                The post to get and its comment count.
                This is returned as an instance of the PostRead
                schema.
        """
        # Get a post
        post = await Post.find_one(Post.id == post_id)
        if not post:
            return None
        # Get the comment count of the post
        comment_count = await Comment.find(Comment.post_id == post_id).count()
        # Add to the PostRead schema
        post_read = PostRead(**post.model_dump(), number_of_comments=comment_count)
        # Return the schema
        return post_read
    
    @staticmethod
    async def get_specific_posts(skip: int, limit: int) -> List[PostRead]:
        """
            Get a subset of posts

            Args:
                skip (int): The number of posts to skip
                limit (int): Maximum number of posts to obtain

            Returns:
                A list of posts with the PostRead schema
        """
        posts = await Post.find(skip=skip, limit=limit).to_list()
        post_data = []
        for post in posts:
            # Get the comment count for each post
            comment_count = await Comment.find(Comment.post_id == post.id).count()
            post_read = PostRead(**post.model_dump(), number_of_comments=comment_count)
            post_data.append(post_read)
        return post_data


    @staticmethod
    async def add_posts(post_list: List[dict]) -> List[Post]:
        """
            Create a list of posts into the database.

            Args:
                post_list (List[dict]): The list of posts to be sent

            Returns:
                The list of Post
        """
        posts = [Post(**post) for post in post_list]
        try:
            # Inser many posts at once to the db
            await Post.insert_many(posts)
            return posts
        except Exception as e:
            return e
        
    
    @staticmethod
    async def get_comments_by_post(post_id: int) -> PostCommentRead:
        """
            Get all the comments associated with a post

            Args:
                post_id (int): The id of the post

            Return:
                The post and the comments associated with the post.
                The is returned based on the PostCommentRead schema.
        """

        # Get the post by the post_id
        post = await Post.find_one(Post.id == post_id)
        if not post:
            return None
        # Get all the comments by the post_id
        comments = await Comment.find(Comment.post_id == post_id).to_list()
        # Post and the comment using the PostCommentRead schema
        post_comments = PostCommentRead(**post.model_dump(), comments=comments)
        return post_comments