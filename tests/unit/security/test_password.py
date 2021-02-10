from drivr.security.password import hash_password, verify_password

MODULE = "drivr.security.password"


class TestHashPassword:
    def test_should_call_argon2_hash(self, faker, mocker):
        plain_text = faker.word()
        hash_return = faker.sha256()

        argon2_hash = mocker.patch(
            f"{MODULE}.argon2.hash", return_value=hash_return
        )

        actual = hash_password(plain_text=plain_text)

        assert hash_return == actual
        argon2_hash.assert_called_once()


class TestVerifyPassword:
    def test_should_call_argon2_verify(self, faker, mocker):
        plain_text = faker.word()
        hashed_password = faker.sha256()
        verify_return = faker.boolean()

        argon2_verify = mocker.patch(
            f"{MODULE}.argon2.verify",
            return_value=verify_return,
        )

        actual = verify_password(
            plain_text=plain_text,
            hashed_password=hashed_password,
        )

        assert verify_return == actual
        argon2_verify.assert_called_once()
