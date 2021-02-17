import pytest
from fastapi.exceptions import HTTPException
from jwt import PyJWTError
from pydantic import ValidationError

from drivr.api.deps import (
    db_session,
    get_authenticated_active_user,
    get_authenticated_moderator,
    get_authenticated_user,
)
from tests.unit.factories import UserFactory

MODULE = "drivr.api.deps"


class TestDbSession:
    def test_should_call_session_local_and_close_db_session_on_yield(
        self,
        mocker,
    ):
        session_local = mocker.patch(f"{MODULE}.db.SessionLocal")

        next(db_session())

        session_local.assert_called_once()
        session_local().close.assert_called_once()


class TestGetAuthenticated:
    def test_should_raise_httpexception_403_when_pyjwterror_is_raised(
        self,
        mocker,
        faker,
    ):
        db = mocker.MagicMock()
        token = faker.sha1()
        secret_key = faker.sha1()
        access_token_algorithm = faker.word()

        decode = mocker.patch(f"{MODULE}.decode", side_effect=PyJWTError())
        settings = mocker.patch(f"{MODULE}.core.settings")
        settings.SECRET_KEY = secret_key
        settings.ACCESS_TOKEN_ALGORITHM = access_token_algorithm

        with pytest.raises(HTTPException) as ex:
            get_authenticated_user(db=db, token=token)

        assert ex.value.status_code == 403
        assert ex.value.detail == "Could not validate the user credentials."

        decode.assert_called_once_with(
            jwt=token,
            key=secret_key,
            algorithms=[access_token_algorithm],
        )

    def test_should_raise_httpexception_403_when_validationerror_is_raised(
        self,
        mocker,
        faker,
    ):
        db = mocker.MagicMock()
        token = faker.sha1()
        secret_key = faker.sha1()
        access_token_algorithm = faker.word()

        decode = mocker.patch(
            f"{MODULE}.decode",
            side_effect=ValidationError(
                errors=["errors-stub"],
                model="model-stub",
            ),
        )
        settings = mocker.patch(f"{MODULE}.core.settings")
        settings.SECRET_KEY = secret_key
        settings.ACCESS_TOKEN_ALGORITHM = access_token_algorithm

        with pytest.raises(HTTPException) as ex:
            get_authenticated_user(db=db, token=token)

        assert ex.value.status_code == 403
        assert ex.value.detail == "Could not validate the user credentials."

        decode.assert_called_once_with(
            jwt=token,
            key=secret_key,
            algorithms=[access_token_algorithm],
        )

    def test_should_raise_httpexception_404_when_user_is_not_found(
        self,
        mocker,
        faker,
    ):
        db = mocker.MagicMock()
        token = faker.sha1()
        sub = faker.pyint()
        secret_key = faker.sha1()
        access_token_algorithm = faker.word()

        payload = {"sub": sub}
        decode = mocker.patch(f"{MODULE}.decode", return_value=payload)
        get = mocker.patch(f"{MODULE}.crud.users.get", return_value=None)
        settings = mocker.patch(f"{MODULE}.core.settings")
        settings.SECRET_KEY = secret_key
        settings.ACCESS_TOKEN_ALGORITHM = access_token_algorithm

        with pytest.raises(HTTPException) as ex:
            get_authenticated_user(db=db, token=token)

        assert ex.value.status_code == 404
        assert ex.value.detail == "User not found."

        decode.assert_called_once_with(
            jwt=token,
            key=secret_key,
            algorithms=[access_token_algorithm],
        )

        get.assert_called_once_with(db=db, id=sub)

    def test_should_the_user_object_when_it_exists_in_database(
        self,
        mocker,
        faker,
    ):
        db = mocker.MagicMock()
        token = faker.sha1()
        sub = faker.pyint()
        secret_key = faker.sha1()
        access_token_algorithm = faker.word()
        user = UserFactory()

        payload = {"sub": sub}
        decode = mocker.patch(f"{MODULE}.decode", return_value=payload)
        get = mocker.patch(f"{MODULE}.crud.users.get", return_value=user)
        settings = mocker.patch(f"{MODULE}.core.settings")
        settings.SECRET_KEY = secret_key
        settings.ACCESS_TOKEN_ALGORITHM = access_token_algorithm

        actual_user = get_authenticated_user(db=db, token=token)
        assert actual_user == user

        decode.assert_called_once_with(
            jwt=token,
            key=secret_key,
            algorithms=[access_token_algorithm],
        )

        get.assert_called_once_with(db=db, id=sub)


class TestGetAuthenticatedActiveUser:
    def test_should_raise_httpexception_401_when_user_is_not_active(self):
        user = UserFactory(active=False)

        with pytest.raises(HTTPException) as ex:
            get_authenticated_active_user(user=user)

        assert ex.value.status_code == 401
        assert ex.value.detail == "The user is inactive."

    def test_should_the_user_when_it_is_active(self):
        user = UserFactory(active=True)
        assert user == get_authenticated_active_user(user=user)


class TestGetAuthenticatedModerator:
    def test_should_raise_httpexception_401_when_user_is_not_a_moderator(self):
        user = UserFactory(moderator=False)

        with pytest.raises(HTTPException) as ex:
            get_authenticated_moderator(user=user)

        assert ex.value.status_code == 401
        assert (
            ex.value.detail == "You must be moderator to perform this action."
        )

    def test_should_the_user_when_it_is_active(self):
        user = UserFactory(moderator=True)
        assert user == get_authenticated_moderator(user=user)
