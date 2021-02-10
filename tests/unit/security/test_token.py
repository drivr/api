from freezegun import freeze_time

from drivr.security.token import create_access_token

MODULE = "drivr.security.token"


class TestCreateAccessToken:
    def test_should_encode_subject_with_correct_params(self, faker, mocker):
        subject = faker.word()
        secret_key = faker.sha1()
        token_algorithmn = faker.word()
        token_minute_expiration = faker.pyint(min_value=0, max_value=59)
        encoded_token = faker.word()

        settings = mocker.patch(f"{MODULE}.core.settings")
        settings.SECRET_KEY = secret_key
        settings.ACCESS_TOKEN_ALGORITHM = token_algorithmn
        settings.ACCESS_TOKEN_EXPIRATION = token_minute_expiration

        timedelta = mocker.patch(f"{MODULE}.timedelta")
        encode = mocker.patch(
            f"{MODULE}.encode",
            return_value=encoded_token,
        )

        with freeze_time(
            "Jan 7th, 2021",
        ):
            assert encoded_token == create_access_token(subject=subject)

        timedelta.assert_called_once_with(minutes=token_minute_expiration)
        encode.assert_called_once_with(
            {"exp": mocker.ANY, "sub": subject},
            key=secret_key,
            algorithm=token_algorithmn,
        )
