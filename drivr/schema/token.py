from typing import Optional

from pydantic.main import BaseModel


class TokenPayload(BaseModel):
    """The payload from JWT."""

    sub: Optional[int] = None


class Token(BaseModel):
    """The response payload to expose."""

    access_token: str
    token_type: str
