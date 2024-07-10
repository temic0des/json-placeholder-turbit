from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

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

    pass

class UserCreate(UserBase):

    name: str
    username: str
    email: EmailStr
    address: Address
    phone: str
    website: str
    company: Company

class UserRead(UserBase):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: str
    username: str
    email: EmailStr
    phone: str
    address: Address
    website: str
    company: Company

class UserUpdate(UserBase):

    model_config = ConfigDict(arbitrary_types_allowed=True)

    name: Optional[str] = None
    username: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[Address] = None
    website: Optional[str] = None
    company: Optional[Company] = None