from typing import Annotated
from beanie import Document, Indexed, Insert, Replace, before_event
from pydantic import Field


class Post(Document):

    id: int = Field(default_factory=int, alias='_id')
    user_id: int = Field(..., alias='userId')
    title: Annotated[str, Indexed(unique=True)]
    body: str

    def __str__(self) -> str:
        return self.title
    
    @before_event(Insert, Replace)
    def lowercase_title(self):
        self.title = self.title.lower()

    class Settings:
        name = 'posts'