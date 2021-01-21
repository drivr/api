__ARGON2__ = "drivr.core.security.argon2"


from drivr import core


def test_password_hash_should_call_argon2_hash(
    faker,
    mocker,
):
    plain_text = faker.word()
    hash_return = faker.sha256()

    argon2_hash = mocker.patch(f"{__ARGON2__}.hash", return_value=hash_return)

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
        f"{__ARGON2__}.verify",
        return_value=verify_return,
    )

    actual = core.verify_password(
        plain_text=plain_text,
        hashed_password=hashed_password,
    )

    assert verify_return == actual
    argon2_verify.assert_called_once()
