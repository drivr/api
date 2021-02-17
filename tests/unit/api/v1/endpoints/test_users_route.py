from drivr import schema
from drivr.api import deps
from tests.unit.factories import UserFactory

MODULE = "drivr.api.v1.endpoints.users"


class TestGet:
    def test_should_query_for_all_users_using_default_query_params(
        self,
        mocker,
        client,
    ):
        db = mocker.MagicMock()
        user = UserFactory()

        all = mocker.patch(f"{MODULE}.crud.users.all", return_value=[])
        client.app.dependency_overrides[
            deps.get_authenticated_active_user
        ] = lambda: user
        client.app.dependency_overrides[deps.db_session] = lambda: db

        response = client.get(
            "/users/",
        )

        assert response.status_code == 200
        assert response.json() == []

        all.assert_called_once_with(db=db, skip=0, limit=100)

    def test_should_query_for_all_users_using_the_query_params_specified(
        self,
        faker,
        mocker,
        client,
    ):
        db = mocker.MagicMock()
        skip = faker.pyint()
        limit = faker.pyint()

        user = UserFactory()

        all = mocker.patch(f"{MODULE}.crud.users.all", return_value=[])
        client.app.dependency_overrides[
            deps.get_authenticated_active_user
        ] = lambda: user
        client.app.dependency_overrides[deps.db_session] = lambda: db

        response = client.get("/users/", params={"limit": limit, "skip": skip})

        assert response.status_code == 200
        assert response.json() == []

        all.assert_called_once_with(db=db, skip=skip, limit=limit)


class TestPost:
    def test_should_return_422_when_request_schema_is_invalid(self, client):
        client.post("/users/", json={}).status_code == 422

    def test_should_return_409_conflict_if_email_is_already_registed(
        self,
        mocker,
        client,
    ):
        db = mocker.MagicMock()
        user = UserFactory()

        crud = mocker.patch(f"{MODULE}.crud.users")
        crud.get_by_email.return_value = user

        client.app.dependency_overrides[deps.db_session] = lambda: db

        response = client.post(
            "/users/",
            json={
                "email": user.email,
                "password": user.password,
            },
        )

        assert response.status_code == 409
        assert response.json() == {
            "detail": f"The email '{user.email} is alredy registered."
        }

        crud.get_by_email.assert_called_once_with(db=db, email=user.email)
        crud.create.assert_not_called()

    def test_should_return_201_with_created_user_data(
        self,
        mocker,
        client,
    ):
        db = mocker.MagicMock()
        user = UserFactory()
        request_payload = {
            "email": user.email,
            "password": user.password,
        }

        crud = mocker.patch(f"{MODULE}.crud.users")
        crud.get_by_email.return_value = None
        crud.create.return_value = user

        client.app.dependency_overrides[deps.db_session] = lambda: db

        response = client.post("/users/", json=request_payload)

        assert response.status_code == 201
        assert response.json() == {
            "active": user.active,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
            "email": user.email,
            "moderator": user.moderator,
        }

        crud.get_by_email.assert_called_once_with(db=db, email=user.email)
        crud.create.assert_called_once_with(
            db=db,
            schema=schema.UserCreate(**request_payload),
        )


class TestPut:
    def test_should_return_422_when_request_schema_is_invalid(self, client):
        client.put("/users/", json={}).status_code == 422

    def test_should_return_404_when_user_is_not_found(
        self,
        mocker,
        client,
    ):

        db = mocker.MagicMock()
        user = UserFactory()
        moderator = UserFactory(moderator=True)

        request_payload = {
            "email": user.email,
            "password": user.password,
        }

        crud = mocker.patch(f"{MODULE}.crud.users")
        crud.get.return_value = None

        client.app.dependency_overrides[deps.db_session] = lambda: db
        client.app.dependency_overrides[
            deps.get_authenticated_moderator
        ] = lambda: moderator

        response = client.put(f"/users/{user.id}", json=request_payload)

        assert response.status_code == 404
        assert response.json() == {
            "detail": "No user found for the ID provided."
        }

        crud.get.assert_called_once_with(db=db, id=user.id)
        crud.update.assert_not_called()

    def test_should_return_200_with_updated_user_data(
        self,
        mocker,
        client,
    ):

        db = mocker.MagicMock()
        user = UserFactory()
        moderator = UserFactory(moderator=True)

        request_payload = {
            "email": user.email,
            "password": user.password,
        }

        crud = mocker.patch(f"{MODULE}.crud.users")
        crud.get.return_value = user
        crud.update.return_value = user

        client.app.dependency_overrides[deps.db_session] = lambda: db
        client.app.dependency_overrides[
            deps.get_authenticated_moderator
        ] = lambda: moderator

        response = client.put(f"/users/{user.id}", json=request_payload)

        assert response.status_code == 200
        assert response.json() == {
            "active": user.active,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
            "email": user.email,
            "moderator": user.moderator,
        }

        crud.get.assert_called_once_with(db=db, id=user.id)
        crud.update.assert_called_once_with(
            db=db,
            user=user,
            schema=schema.UserUpdate(**request_payload),
        )


class TestDelete:
    def test_should_return_422_when_request_schema_is_invalid(self, client):
        client.delete("/users/", json={}).status_code == 422

    def test_should_return_404_when_user_is_not_found(
        self,
        mocker,
        client,
    ):

        db = mocker.MagicMock()
        user = UserFactory()
        moderator = UserFactory(moderator=True)

        crud = mocker.patch(f"{MODULE}.crud.users")
        crud.get.return_value = None

        client.app.dependency_overrides[deps.db_session] = lambda: db
        client.app.dependency_overrides[
            deps.get_authenticated_moderator
        ] = lambda: moderator

        response = client.delete(f"/users/{user.id}")

        assert response.status_code == 404
        assert response.json() == {
            "detail": "No user found for the ID provided."
        }

        crud.get.assert_called_once_with(db=db, id=user.id)
        crud.remove.assert_not_called()

    def test_should_return_200_with_removed_user_data(
        self,
        mocker,
        client,
    ):

        db = mocker.MagicMock()
        user = UserFactory()
        moderator = UserFactory(moderator=True)

        crud = mocker.patch(f"{MODULE}.crud.users")
        crud.get.return_value = user
        crud.remove.return_value = user

        client.app.dependency_overrides[deps.db_session] = lambda: db
        client.app.dependency_overrides[
            deps.get_authenticated_moderator
        ] = lambda: moderator

        response = client.delete(f"/users/{user.id}")

        assert response.status_code == 200
        assert response.json() == {
            "active": user.active,
            "created_at": user.created_at.isoformat(),
            "updated_at": user.updated_at.isoformat(),
            "email": user.email,
            "moderator": user.moderator,
        }

        crud.get.assert_called_once_with(db=db, id=user.id)
        crud.remove.assert_called_once_with(db=db, model=user)
