from typing import Optional

from sqlalchemy.orm.session import Session

from drivr import model, schema

from .crud_base import CRUDBase


class CRUDUsers(
    CRUDBase[
        model.User,
        schema.UserCreate,
        schema.UserUpdate,
    ]
):
    def get_by_email(self, db: Session, email: str) -> Optional[model.User]:
        return db.query(model.User).filter_by(email=email).first()


users = CRUDUsers(model=model.User)
