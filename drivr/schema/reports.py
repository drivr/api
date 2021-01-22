from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReportBase(BaseModel):
    """The shared attrs related to user model."""

    markdown: str
    html: str


class ReportCreate(ReportBase):
    """The schema used to create the report model."""


class ReportUpdate(ReportBase):
    """The schema used to update the report model."""

    markdown: Optional[str] = None
    html: Optional[str] = None


class Report(ReportBase):
    """The schema used to expose the report model."""

    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
