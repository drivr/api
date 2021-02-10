from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.ext.declarative.api import declared_attr


@as_declarative()
class Entity:
    """The base class used to map the database entities."""

    __name__: str

    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    def __repr__(self) -> str:
        return str(self.__dict__)
