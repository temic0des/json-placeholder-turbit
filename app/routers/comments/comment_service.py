from typing import List
from app.routers.comments.comment_interface import IComment
from app.routers.comments.comment_model import Comment


class CommentService(IComment):

    @staticmethod
    async def add_comments(comment_list: List[dict]) -> List[Comment]:
        comments = [Comment(**comment) for comment in comment_list]
        try:
            await Comment.insert_many(comments)
            return comments
        except Exception as e:
            return e
        
    
    @staticmethod
    async def get_all_comments() -> List[Comment]:
        all_comments = await Comment.find_all().to_list()
        return all_comments
    
    @staticmethod
    async def get_specific_comments(skip: int, limit: int) -> List[Comment]:
        comments = await Comment.find(skip=skip, limit=limit).to_list()
        return comments
    
    @staticmethod
    async def get_comment_by_id(comment_id: int) -> Comment:
        comment = await Comment.find_one(Comment.id == comment_id)
        return comment