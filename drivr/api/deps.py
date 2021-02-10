from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode
from pydantic import ValidationError
from sqlalchemy.orm.session import Session

from drivr import core, crud, db, model, schema

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login")


def db_session() -> Generator:
    """Get the database session."""

    session = db.SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_authenticated_user(
    db: Session = Depends(db_session),
    token: str = Depends(reusable_oauth2),
) -> Optional[model.User]:
    """Get the current authenticated user."""

    try:
        payload = decode(
            jwt=token,
            key=core.settings.SECRET_KEY,
            algorithms=[core.settings.ACCESS_TOKEN_ALGORITHM],
        )
        token_payload = schema.TokenPayload(**payload)
    except (PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate the user credentials.",
        )

    user = crud.users.get(db=db, id=token_payload.sub)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    return user


def get_authenticated_active_user(
    user: model.User = Depends(get_authenticated_user),
) -> Optional[model.User]:
    """Get the current active authenticated moderator."""

    if not user.active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user is inactive.",
        )

    return user


def get_authenticated_moderator(
    user: model.User = Depends(get_authenticated_user),
) -> Optional[model.User]:
    """Get the current authenticated moderator."""

    if not user.moderator:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="You must be moderator to perform this action.",
        )

    return user
