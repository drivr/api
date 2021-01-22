from typing import List

from .reports import Report
from .users import User


class UserWithReports(User):
    """The user schema with reports included."""

    reports: List[Report]

    class Config:
        orm_mode = True


class ReportWithUser(Report):
    """The report schema with the owner user included."""

    user: User

    class Config:
        orm_mode = True
