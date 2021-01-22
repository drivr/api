from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ReportBase(BaseModel):
    markdown: str
    html: str


class ReportCreate(ReportBase):
    ...


class ReportUpdate(ReportBase):
    markdown: Optional[str] = None
    html: Optional[str] = None


class Report(ReportBase):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
