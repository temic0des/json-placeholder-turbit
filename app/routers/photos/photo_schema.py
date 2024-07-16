from typing import Annotated
from pydantic import BaseModel, ConfigDict, Field, UrlConstraints
from pydantic_core import Url


class PhotoBase(BaseModel):

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    album_id: int = Field(..., alias="albumId")
    url: Annotated[Url, UrlConstraints(max_length=2083, allowed_schemes=["http", "https"])]
    thumbnail_url: Annotated[Url, Field(alias='thumbnailUrl'), UrlConstraints(max_length=2083, allowed_schemes=["http", "https"])]

class PhotoRead(PhotoBase):

    pass

class PhotoCreate(PhotoBase):

    pass