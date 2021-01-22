from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.networks import EmailStr


class UserBase(BaseModel):
    """The shared attrs related to user model."""

    email: EmailStr


class UserCreate(UserBase):
    """The schema used to create the user model."""

    password: str


class UserUpdate(UserBase):
    """The schema used to update the user model."""

    email: Optional[EmailStr] = None
    password: Optional[str] = None


class User(UserBase):
    """The schema used to expose the user model."""

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
