from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

_engine = None


def create_db_engine(connection: str):
    global _engine
    if _engine is None:
        _engine = create_engine(connection)
    return _engine


def create_db_session():
    session = sessionmaker(
        bind=_engine,
        autocommit=False,
        autoflush=False,
    )
    return session()
