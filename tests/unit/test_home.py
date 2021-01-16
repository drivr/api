from requests.sessions import Session


def test_should_return_the_hello_message(client: Session):
    expected_http_status = 200
    expected_json = {"message": "Hello from drivr's API."}

    response = client.get("/")

    assert response.status_code == expected_http_status
    assert response.json() == expected_json
