from datetime import datetime, timedelta

from jwt import encode

from drivr import core


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
