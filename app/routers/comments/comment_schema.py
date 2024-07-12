from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CommentBase(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    name: str
    body: str
    email: EmailStr
    post_id: int = Field(..., alias='postId')

class CommentCreate(CommentBase):

    pass

class CommentRead(CommentBase):

    pass