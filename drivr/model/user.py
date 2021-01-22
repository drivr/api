from sqlalchemy import sql
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import DateTime, Integer, String

from drivr.db.entity import Entity


class User(Entity):
    """The attribute from 'user' table."""

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=sql.func.now(),
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=sql.func.now(),
        onupdate=sql.func.now(),
    )

    reports = relationship(
        "Report",
        backref="user",
        passive_deletes=True,
    )
