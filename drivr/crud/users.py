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
    """CRUD actions associated to the 'user' entity."""

    def get_by_email(self, db: Session, email: str) -> Optional[model.User]:
        """
        Query for an user based on the email address.

        Args:
            db: the database session.
            email: the email address.

        Returns:
            The entity associated to the email address provided if it exists,
            otherwise `None` is returned.
        """
        return db.query(model.User).filter_by(email=email).first()


users = CRUDUsers(model=model.User)
