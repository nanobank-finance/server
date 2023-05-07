import time
from tests import client


def test_get_open_loans() -> None:
    """Test /loans/open GET endpoint."""
    # Given
    recent = False

    # Act
    response = client.get(f"/loans/open?recent={recent}")

    # Assert
    assert response.status_code == 200


def test_get_accepted_loans() -> None:
    """Test /loans/accepted GET endpoint."""
    # Given
    recent = False

    # Act
    response = client.get(f"/loans/accepted?recent={recent}")

    # Assert
    assert response.status_code == 200


def test_get_my_open_loans() -> None:
    """Test /loans/user/self/open GET endpoint."""
    # Given
    recent = False

    # Act
    response = client.get(f"/loans/user/self/open?recent={recent}")

    # Assert
    assert response.status_code == 200


def test_get_my_accepted_loans() -> None:
    """Test /loans/user/self/accepted GET endpoint."""
    # Given
    recent = False

    # Act
    response = client.get(f"/loans/user/self/accepted?recent={recent}")

    # Assert
    assert response.status_code == 200


def test_get_their_open_loans() -> None:
    """Test /loans/user/their/open GET endpoint."""
    # Given
    recent = False
    them = 123

    # Act
    response = client.get(f"/loans/user/their/open?them={them}&recent={recent}")

    # Assert
    assert response.status_code == 200


def test_get_their_accepted_loans() -> None:
    """Test /loans/user/their/accepted GET endpoint."""
    # Given
    recent = False
    them = 123

    # Act
    response = client.get(
        f"/loans/user/their/accepted?them={them}&recent={recent}"
    )

    # Assert
    assert response.status_code == 200


def test_get_loan() -> None:
    """Test /loan GET endpoint."""
    # Given
    loan_id = 123

    # Act
    response = client.get(f"/loan?loan_id={loan_id}")

    # Assert
    assert response.status_code == 200


def test_create_loan() -> None:
    """Test the /loan POST endpoint."""
    # Given
    borrower = 1000
    principal = 1000
    interest = 1.1
    duration = 30
    payments = 30
    # set expiry to 1 day from now in nanoseconds
    expiry = int(time.time() + 86400) * 1000000000

    # send the request with all the parameters
    response = client.post(f"loan?borrower={borrower}&principal={principal}&interest={interest}&duration={duration}&payments={payments}&expiry={expiry}")

    # Assert
    assert response.status_code == 200
    assert response.json()["success"] is True