from drivr import model
from drivr.crud.crud_users import CRUDUsers
from tests.unit.factories import UserFactory

MODULE = "drivr.crud.crud_users"


class TestByEmail:
    def test_should_query_filtering_by_email_provided(
        self,
        faker,
        mocker,
    ):
        email = faker.email()
        db = mocker.MagicMock()

        crud_users = CRUDUsers(model=model.User)
        crud_users.get_by_email(db=db, email=email)

        db.query.assert_called_once_with(model.User)
        db.query().filter_by.assert_called_once_with(email=email)
        db.query().filter_by().first.assert_called_once()


class TestAuthenticate:
    def test_should_return_none_when_user_does_not_exist(
        self,
        faker,
        mocker,
    ):
        email = faker.email()
        password = faker.sha1()
        db = mocker.MagicMock()

        get_by_email = mocker.patch.object(
            CRUDUsers,
            "get_by_email",
            return_value=None,
        )

        actual_user = CRUDUsers(model=model.User).authenticate(
            db=db,
            email=email,
            password=password,
        )

        assert actual_user is None
        get_by_email.assert_called_once_with(db=db, email=email)

    def test_should_return_none_when_password_hash_does_not_match(
        self,
        faker,
        mocker,
    ):
        user = UserFactory()

        email = faker.email()
        password = faker.sha1()
        db = mocker.MagicMock()

        verify_password = mocker.patch(
            f"{MODULE}.security.verify_password",
            return_value=False,
        )

        get_by_email = mocker.patch.object(
            CRUDUsers,
            "get_by_email",
            return_value=user,
        )

        actual_user = CRUDUsers(model=model.User).authenticate(
            db=db,
            email=email,
            password=password,
        )
        assert actual_user is None

        get_by_email.assert_called_once_with(db=db, email=email)
        verify_password.assert_called_once_with(
            plain_text=password,
            hashed_password=user.password,
        )

    def test_should_return_the_user_object_when_user_exists_and_password_hash_match(
        self,
        faker,
        mocker,
    ):
        user = UserFactory()

        email = faker.email()
        password = faker.sha1()
        db = mocker.MagicMock()

        get_by_email = mocker.patch.object(
            CRUDUsers,
            "get_by_email",
            return_value=user,
        )
        verify_password = mocker.patch(
            f"{MODULE}.security.verify_password",
            return_value=True,
        )

        actual_user = CRUDUsers(model=model.User).authenticate(
            db=db,
            email=email,
            password=password,
        )

        assert actual_user == user

        get_by_email.assert_called_once_with(db=db, email=email)
        verify_password.assert_called_once_with(
            plain_text=password,
            hashed_password=user.password,
        )
