from typing import List
from pydantic import BaseModel, ConfigDict, Field

from app.common.schemas.user_read import UserCommonRead
from app.routers.comments.comment_model import Comment

class PostBase(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    title: str
    body: str

class PostCreate(PostBase):
    
    user_id: int = Field(..., alias='userId')

class PostRead(PostBase):

    number_of_comments: int = 0
    user: int = Field(..., alias='userId')

class PostCommentRead(PostBase):

    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True)

    comments: List[Comment] = []