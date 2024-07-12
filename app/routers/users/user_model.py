from typing import Annotated
from beanie import Document, Indexed, Insert, Replace, before_event
from pydantic import EmailStr, Field
from app.routers.users.user_schema import Address, Company

class User(Document):

    id: int = Field(default_factory=int, alias='_id')
    name: str
    username: Annotated[str, Indexed(unique=True)]
    email: Annotated[EmailStr, Indexed(unique=True)]
    address: Address
    phone: Annotated[str, Indexed(unique=True)]
    website: str
    company: Company

    @staticmethod
    async def get_user_by_id(id):
        user = await User.get(id)
        return user

    def __str__(self) -> str:
        return self.email
    
    @before_event(Insert, Replace)
    def capitalize_name(self):
        self.name = self.name.capitalize()

    @before_event(Insert, Replace)
    def capitalize_username(self):
        self.username = self.username.capitalize()

    @before_event(Insert, Replace)
    def capitalize_email(self):
        self.email = self.email.capitalize()

    @before_event(Insert, Replace)
    def capitalize_street(self):
        self.address.street = self.address.street.capitalize()

    @before_event(Insert, Replace)
    def capitalize_street(self):
        self.address.suite = self.address.suite.capitalize()

    @before_event(Insert, Replace)
    def capitalize_street(self):
        self.address.city = self.address.city.capitalize()

    class Settings:
        name = 'users'