from typing import List, Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.routers.albums.album_schema import AlbumRead
from app.routers.posts.post_schema import PostRead

class Geo(BaseModel):

    lat: str
    lng: str

class Company(BaseModel):

    model_config = ConfigDict(populate_by_name=True)

    name: str
    catch_phrase: str = Field(..., alias='catchPhrase')
    bs: str

class Address(BaseModel):

    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo

class UserBase(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    username: str
    email: EmailStr
    address: Address
    phone: str
    website: str
    company: Company

class UserCreate(UserBase):

    pass

class UserRead(UserBase):

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., alias="_id")
    number_of_posts: int = 0

class UserUpdate(BaseModel):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[Address] = None
    website: Optional[str] = None
    company: Optional[Company] = None

class UserPostRead(UserBase):

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., alias="_id")
    posts: List[PostRead] = []

class UserAlbumRead(UserBase):

    model_config = ConfigDict(populate_by_name=True)

    id: int = Field(..., alias="_id")
    albums: List[AlbumRead] = []