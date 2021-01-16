import pytest


@pytest.fixture
def client():
    from fastapi.testclient import TestClient

    from drivr import app

    return TestClient(app=app)
