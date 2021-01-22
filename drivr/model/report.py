from sqlalchemy import sql
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import DateTime, Integer, Text

from drivr.db.entity import Entity


class Report(Entity):
    """The attribute from 'report' table."""

    id = Column(Integer, primary_key=True, index=True)
    markdown = Column(Text, nullable=False)
    html = Column(Text, nullable=False)
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

    user_id = Column(ForeignKey("user.id", ondelete="CASCADE"))
