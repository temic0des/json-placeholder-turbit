from typing import Annotated
from beanie import Document, Indexed, Insert, Replace, before_event
from pydantic import Field, UrlConstraints
from pydantic_core import Url


class Photo(Document):

    id: int = Field(default_factory=int, alias='_id')
    album_id: int = Field(..., alias="albumId")
    title: Annotated[str, Indexed(unique=True)]
    url: Annotated[Url, UrlConstraints(max_length=2083, allowed_schemes=["http", "https"])]
    thumbnail_url: Annotated[Url, UrlConstraints(max_length=2083, allowed_schemes=["http", "https"])]

    def __str__(self) -> str:
        return self.title
    
    @before_event(Insert, Replace)
    def lower_title(self):
        self.title = self.title.capitalize()

    class Settings:
        name = "photos"