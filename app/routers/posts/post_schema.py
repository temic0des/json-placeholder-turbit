from pydantic import BaseModel, ConfigDict, Field
class PostBase(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    title: str
    body: str
    user_id: int = Field(..., alias='userId')

class PostCreate(PostBase):
    pass

class PostRead(PostBase):

    model_config = ConfigDict(arbitrary_types_allowed=True)