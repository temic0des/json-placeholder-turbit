from pydantic import BaseModel, ConfigDict, Field


class TodoBase(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    user_id: int = Field(..., alias='userId')
    title: str
    completed: bool = False

class TodoCreate(TodoBase):

    pass

class TodoUpdate(TodoBase):

    pass

class TodoRead(TodoBase):

    pass