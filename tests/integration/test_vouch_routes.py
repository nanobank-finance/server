from tests import client


def test_submit_vouch() -> None:
    """Test /vouch POST endpoint."""
    # Given
    vouchee = "123"

    # Act
    response = client.post(f"/vouch?vouchee={vouchee}")

    # Assert
    assert response.status_code == 200
    assert response.json()["success"] is True


def test_get_all_vouches() -> None:
    """Test /vouch GET endpoint."""
    # Act
    response = client.get("/vouch")

    # Assert
    assert response.status_code == 200
