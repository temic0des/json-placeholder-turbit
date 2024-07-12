from beanie import Document
from pydantic import EmailStr, Field


class Comment(Document):

    id: int = Field(default_factory=int, alias='_id')
    post_id: int = Field(..., alias='postId')
    name: str
    email: EmailStr
    body: str

    def __str__(self) -> EmailStr:
        return self.email
    
    class Settings:
        name = 'comments'