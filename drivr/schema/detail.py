from pydantic import BaseModel


class Detail(BaseModel):
    """The schema for HTTException details."""

    detail: str
