from pydantic.types import SecretStr

from drivr import model, schema
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

    def test_should_return_the_user_object_when_it_exist_and_password_match(
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


class TestCreate:
    def test_should_commit_and_refresh_the_create_entity(self, faker, mocker):
        hashed_password = faker.sha1()

        db = mocker.MagicMock()
        created_user = UserFactory(password=SecretStr(hashed_password))

        mocker.patch(f"{MODULE}.model.User", return_value=created_user)
        hash_password = mocker.patch(
            f"{MODULE}.hash_password",
            return_value=hashed_password,
        )

        user_schema = schema.UserCreate(
            email=faker.email(), password=faker.word()
        )

        actual_user = CRUDUsers(model=model.User).create(
            db=db, schema=user_schema
        )

        assert actual_user == created_user
        hash_password.assert_called_once_with(created_user.password)
        db.add.assert_called_once_with(created_user)
        db.commit.assert_called_once()
        db.refresh.assert_called_once_with(created_user)


class TestUpdate:
    def test_should_update_the_user_with_the_schema_data_provided(
        self,
        mocker,
    ):
        db = mocker.MagicMock()
        user = UserFactory()

        hash_password = mocker.patch(f"{MODULE}.hash_password")
        update_method = mocker.patch(
            f"{MODULE}.CRUDBase.update",
            return_value=user,
        )

        user_schema = mocker.MagicMock()
        user_schema.password = None

        actual_user = CRUDUsers(model=model.User).update(
            db=db,
            user=user,
            schema=user_schema,
        )

        assert actual_user == user

        update_method.assert_called_once_with(
            db=db,
            model=user,
            schema=user_schema.dict(exclude_unset=True),
        )
        hash_password.assert_not_called()

    def test_should_hash_the_new_password_when_it_is_present_in_schema_data(
        self,
        faker,
        mocker,
    ):
        plain_password = faker.word()
        hashed_password = faker.sha1()
        db = mocker.MagicMock()
        user = UserFactory()

        hash_password = mocker.patch(
            f"{MODULE}.hash_password",
            return_value=hashed_password,
        )
        update_method = mocker.patch(
            f"{MODULE}.CRUDBase.update",
            return_value=user,
        )

        user_schema = mocker.MagicMock()
        user_schema.password.get_secret_value.return_value = plain_password
        user_schema.dict.return_value = {
            "email": user_schema.email,
            "password": hashed_password,
        }

        actual_user = CRUDUsers(model=model.User).update(
            db=db,
            user=user,
            schema=user_schema,
        )

        assert actual_user == user

        user_schema.password.get_secret_value.assert_called_once()
        hash_password.assert_called_once_with(plain_password)
        update_method.assert_called_once_with(
            db=db,
            model=user,
            schema={
                "email": user_schema.email,
                "password": hashed_password,
            },
        )
