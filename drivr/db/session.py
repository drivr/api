from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from drivr import core

engine = create_engine(core.settings.SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)
