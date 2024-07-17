
from typing import List
from pydantic import BaseModel, ConfigDict, Field

from app.routers.photos.photo_schema import PhotoRead


class AlbumBase(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(..., alias='userId')
    title: str

class AlbumRead(AlbumBase):

    pass

class AlbumCreate(AlbumBase):

    pass

class AlbumPhotoRead(AlbumBase):

    photos: List[PhotoRead] = []