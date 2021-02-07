from freezegun import freeze_time

from drivr import core

__SECURITY__ = "drivr.core.security"


def test_password_hash_should_call_argon2_hash(
    faker,
    mocker,
):
    plain_text = faker.word()
    hash_return = faker.sha256()

    argon2_hash = mocker.patch(
        f"{__SECURITY__}.argon2.hash", return_value=hash_return
    )

    actual = core.hash_password(plain_text=plain_text)

    assert hash_return == actual
    argon2_hash.assert_called_once()


def test_password_verify_should_call_argon2_verify(
    faker,
    mocker,
):
    plain_text = faker.word()
    hashed_password = faker.sha256()
    verify_return = faker.boolean()

    argon2_verify = mocker.patch(
        f"{__SECURITY__}.argon2.verify",
        return_value=verify_return,
    )

    actual = core.verify_password(
        plain_text=plain_text,
        hashed_password=hashed_password,
    )

    assert verify_return == actual
    argon2_verify.assert_called_once()


def test_create_access_token_should_encode_subject_with_correct_params(
    faker,
    mocker,
):
    subject = faker.word()
    secret_key = faker.sha1()
    token_algorithmn = faker.word()
    token_minute_expiration = faker.pyint(min_value=0, max_value=59)
    encoded_token = faker.word()

    settings = mocker.patch(f"{__SECURITY__}.core.settings")
    settings.SECRET_KEY = secret_key
    settings.ACCESS_TOKEN_ALGORITHM = token_algorithmn
    settings.ACCESS_TOKEN_EXPIRATION = token_minute_expiration

    timedelta = mocker.patch(f"{__SECURITY__}.timedelta")
    encode = mocker.patch(
        f"{__SECURITY__}.encode",
        return_value=encoded_token,
    )

    with freeze_time(
        "Jan 7th, 2021",
    ):
        assert encoded_token == core.create_access_token(subject=subject)

    timedelta.assert_called_once_with(minutes=token_minute_expiration)
    encode.assert_called_once_with(
        {"exp": mocker.ANY, "sub": subject},
        key=secret_key,
        algorithm=token_algorithmn,
    )
