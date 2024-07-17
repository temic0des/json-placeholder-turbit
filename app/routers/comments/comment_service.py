from typing import List
from app.routers.comments.comment_interface import IComment
from app.routers.comments.comment_model import Comment


class CommentService(IComment):

    @staticmethod
    async def add_comments(comment_list: List[dict]) -> List[Comment]:
        """
            Inserts a list of comments to the database.

            Args:
                comment_list (List[dict]): Gets a list of commments

            Returns:
                Comments based on the Comment Schema
        """
        comments = [Comment(**comment) for comment in comment_list]
        try:
            # Insert many comments
            await Comment.insert_many(comments)
            return comments
        except Exception as e:
            return e
        
    
    @staticmethod
    async def get_all_comments() -> List[Comment]:
        """
            Get all the comments

            Returns:
                A list of comments
        """
        all_comments = await Comment.find_all().to_list()
        return all_comments
    
    @staticmethod
    async def get_specific_comments(skip: int, limit: int) -> List[Comment]:
        """
            Get a limited list of comments

            Args:
                skip (int): The number of comments to skip
                limit (int): Maximum number of comments to obtain

            Returns:
                A list of comments based on the Comment Model
        """
        comments = await Comment.find(skip=skip, limit=limit).to_list()
        return comments
    
    @staticmethod
    async def get_comment_by_id(comment_id: int) -> Comment:
        """
            Get comment by the id

            Args:
                comment_id (int): The id of the comment to get

            Returns:
                comment based on the Comment Model
        """
        comment = await Comment.find_one(Comment.id == comment_id)
        return comment