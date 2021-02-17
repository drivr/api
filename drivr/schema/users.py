from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic.networks import EmailStr
from pydantic.types import SecretStr


class UserBase(BaseModel):
    """The shared attrs related to user model."""

    email: EmailStr


class UserCreate(UserBase):
    """The schema used to create the user model."""

    password: SecretStr


class UserUpdate(UserBase):
    """The schema used to update the user model."""

    email: Optional[EmailStr] = None
    password: Optional[SecretStr] = None
    moderator: Optional[bool] = None


class User(UserBase):
    """The schema used to expose the user model."""

    moderator: bool
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
