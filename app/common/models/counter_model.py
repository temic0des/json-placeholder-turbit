from typing import Annotated
from beanie import Document, Indexed
from pydantic import Field

class Counter(Document):

    collection_name: Annotated[str, Indexed(unique=True)]
    collection_value: int = Field(default_factory=0)

    class Settings:
        name = "counters"