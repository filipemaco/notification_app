from pydantic import BaseModel

from app.schemas.notification import Notification


class UserBase(BaseModel):
    email: str
    country_code: int
    phone_number: int


class UserCreate(UserBase):
    id: int


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    notifications: list[Notification] = []

    class Config:
        orm_mode = True
