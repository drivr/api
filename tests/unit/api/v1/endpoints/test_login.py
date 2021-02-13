from tests.unit.factories import UserFactory

MODULE = "drivr.api.v1.endpoints.login"


class TestLoginEndpoint:
    def test_should_return_bad_request_when_user_is_not_found(
        self,
        mocker,
        faker,
        client,
    ):

        authenticate = mocker.patch(
            f"{MODULE}.crud.users.authenticate",
            return_value=None,
        )

        email = faker.email()
        password = faker.password()

        response = client.post(
            "/login/",
            data={
                "grant_type": "",
                "username": email,
                "password": password,
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )

        assert response.status_code == 400
        assert response.json() == {"detail": "Incorrect email or password."}

        authenticate.assert_called_once_with(
            db=mocker.ANY,
            email=email,
            password=password,
        )

    def test_should_return_bad_request_when_user_is_not_active(
        self,
        mocker,
        client,
    ):

        user = UserFactory(active=False)
        authenticate = mocker.patch(
            f"{MODULE}.crud.users.authenticate",
            return_value=user,
        )

        response = client.post(
            "/login/",
            data={
                "grant_type": "",
                "username": user.email,
                "password": user.password,
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )

        assert response.status_code == 400
        assert response.json() == {"detail": "Inactive user."}

        authenticate.assert_called_once_with(
            db=mocker.ANY,
            email=user.email,
            password=user.password,
        )

    def test_should_create_access_token_when_user_exists_and_is_active(
        self,
        mocker,
        faker,
        client,
    ):
        user = UserFactory(active=True)
        access_token = faker.sha1()

        authenticate = mocker.patch(
            f"{MODULE}.crud.users.authenticate",
            return_value=user,
        )
        create_access_token = mocker.patch(
            f"{MODULE}.security.create_access_token",
            return_value=access_token,
        )

        response = client.post(
            "/login/",
            data={
                "grant_type": "",
                "username": user.email,
                "password": user.password,
                "scope": "",
                "client_id": "",
                "client_secret": "",
            },
        )

        assert response.status_code == 200
        assert response.json() == {
            "access_token": access_token,
            "token_type": "bearer",
        }

        authenticate.assert_called_once_with(
            db=mocker.ANY,
            email=user.email,
            password=user.password,
        )
        create_access_token.assert_called_once_with(subject=user.id)
