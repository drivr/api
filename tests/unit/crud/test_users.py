from drivr import model
from drivr.crud.users import CRUDUsers


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
