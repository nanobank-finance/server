from fastapi.testclient import TestClient
from unittest.mock import MagicMock

from src.routes.vouch import VouchRouter

from tests import client


def test_submit_vouch():
    # Given
    vouchee = "123"

    # Act
    response = client.post(f"/vouch?vouchee={vouchee}")

    # Assert
    assert response.status_code == 200
    assert response.json()["success"] == True


def test_get_all_vouches():
    # Act
    response = client.get("/vouch")

    # Assert
    assert response.status_code == 200
