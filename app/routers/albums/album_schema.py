
from pydantic import BaseModel, ConfigDict, Field


class AlbumBase(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(..., alias='userId')
    title: str

class AlbumRead(AlbumBase):

    pass

class AlbumCreate(AlbumBase):

    pass