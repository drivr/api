from typing import Optional

from sqlalchemy.orm.session import Session

from drivr import model, schema, security

from .crud_base import CRUDBase


class CRUDUsers(
    CRUDBase[
        model.User,
        schema.UserCreate,
        schema.UserUpdate,
    ]
):
    """CRUD actions associated to the 'user' entity."""

    def authenticate(
        self,
        db: Session,
        email: str,
        password: str,
    ) -> Optional[model.User]:
        """
        Authenticate the user.

        Args:
            db: the database session.
            email: the user email.
            password: the user password.

        Returns:
            The user object, if it exists. Otherwise, None is returned.
        """

        if user := self.get_by_email(db=db, email=email):
            if security.verify_password(
                plain_text=password,
                hashed_password=user.password,
            ):
                return user

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
