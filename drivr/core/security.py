from datetime import datetime, timedelta

from jwt import encode
from passlib.hash import argon2

from drivr import core


def hash_password(plain_text: str) -> str:
    """
    Hash the plain text using argon2 algorithm.

    Args:
        plain_text: the value to be hashed.

    Returns:
        The hashed password.
    """
    return argon2.hash(plain_text)


def verify_password(plain_text: str, hashed_password: str) -> bool:
    """
    Verify the password hash.

    Args:
        plain_text: the plain text to be verified.
        hashed_password: the hashed content.

    Returns:
        True if the plain text match the hashed password, otherwise False.
    """
    return argon2.verify(plain_text, hashed_password)


def create_access_token(subject: str) -> bytes:
    """
    Create the access token.

    Args:
        subject: the content to be encoded in token.

    Returns:
        The encoded token as bytes.
    """

    expires_in = datetime.now() + timedelta(
        minutes=core.settings.ACCESS_TOKEN_EXPIRATION
    )

    return encode(
        {
            "exp": expires_in,
            "sub": subject,
        },
        key=core.settings.SECRET_KEY,
        algorithm=core.settings.ACCESS_TOKEN_ALGORITHM,
    )
