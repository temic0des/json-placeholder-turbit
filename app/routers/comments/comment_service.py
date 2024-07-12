from typing import List
from app.routers.comments.comment_interface import IComment
from app.routers.comments.comment_model import Comment


class CommentService(IComment):

    @staticmethod
    async def add_comments(comment_list: List[dict]) -> List[Comment]:
        comments = [Comment(**comment) for comment in comment_list]
        print("In ADD COMMENTS", comments[0])
        try:
            x = await Comment.insert_many(comments)
            print(x.acknowledged)
            return comments
        except:
            return None
    
    @staticmethod
    async def get_all_comments() -> List[Comment]:
        all_comments = await Comment.find_all().to_list()
        return all_comments
    
    @staticmethod
    async def get_specific_comments(skip: int, limit: int) -> List[Comment]:
        comments = await Comment.find(skip=skip, limit=limit).to_list()
        return comments