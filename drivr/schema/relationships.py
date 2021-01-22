from typing import List

from .reports import Report
from .users import User


class UserWithReports(User):
    reports: List[Report]

    class Config:
        orm_mode = True


class ReportWithUser(Report):
    user: User

    class Config:
        orm_mode = True
