from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

from drivr.db.entity import Entity


class User(Entity):
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
