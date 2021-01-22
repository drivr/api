from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
