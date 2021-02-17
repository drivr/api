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
            if security.password.verify_password(
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

    def create(
        self,
        db: Session,
        schema: schema.UserCreate,
    ) -> Optional[model.User]:
        """
        Persist a new user.

        Args:
            db: the database session.
            schema: the schema for create the new user.

        Returns:
            The created user.
        """
        user = model.User(**schema.dict())
        user.password = security.password.hash_password(
            user.password.get_secret_value()
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    def update(
        self,
        db: Session,
        user: model.User,
        schema: schema.UserUpdate,
    ) -> model.User:
        """
        Update an existing user.

        Args:
            - db: the database session.
            - entity: the entity to be updated.
            - schema: the data used to update the user entity.

        Returns:
            - the updated user entity.
        """

        update_data = schema.dict(exclude_unset=True)

        if schema.password:
            hashed_password = security.password.hash_password(
                schema.password.get_secret_value()
            )
            del update_data["password"]
            update_data["password"] = hashed_password

        return super().update(db=db, model=user, schema=update_data)


users = CRUDUsers(model=model.User)
