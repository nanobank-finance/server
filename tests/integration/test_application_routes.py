# """Test src/routes/application.py."""
# from typing import Dict

# import pytest

# from tests import client

# base_url = "http://127.0.0.1:8000"


# @pytest.fixture
# def user_token() -> Dict[str, str]:
#     """Test access token."""
#     return {"access_token": "your_access_token"}


# def test_submit_loan_application(user_token: Dict[str, str]) -> None:
#     """Test /loan/application POST endpoint."""
#     # Given
#     asking = 1000

#     # When
#     response = client.post(
#         f"{base_url}/loan/application?asking={asking}",
#         headers=user_token
#     )

#     # Then
#     assert response.status_code == 200
#     assert response.json()["success"] is True


# def test_get_all_loan_applications(user_token: Dict[str, str]) -> None:
#     """Test /loan/application GET endpoint."""
#     # Given
#     recent = False

#     # When
#     response = client.get(
#         f"{base_url}/loan/application?recent={recent}",
#         headers=user_token
#     )

#     # Then
#     assert response.status_code == 200


# def test_get_my_loan_applications(user_token: Dict[str, str]) -> None:
#     """Test loan/application/user GET endpoint."""
#     # Given
#     recent = False

#     # When
#     response = client.get(
#         f"{base_url}/loan/application/user/self?recent={recent}",
#         headers=user_token
#     )

#     # Then
#     assert response.status_code == 200


# def test_get_their_loan_applications(user_token: Dict[str, str]) -> None:
#     """Test loan/application/user/other GET endpoint."""
#     # Given
#     recent = False
#     them = 123

#     # When
#     response = client.get(
#         f"{base_url}/loan/application/user/other?them={them}&recent={recent}",
#         headers=user_token
#     )

#     # Then
#     assert response.status_code == 200


# def test_withdraw_loan_application(user_token: Dict[str, str]) -> None:
#     """Test /loan/application/{application} DELETE endpoint."""
#     # Given
#     asking = 1000
#     recent = True

#     # When

#     # create the loan application
#     response = client.post(
#         f"{base_url}/loan/application?asking={asking}",
#         headers=user_token
#     )
#     assert response.status_code == 200

#     # get the loan application
#     response = client.get(
#         f"{base_url}/loan/application/user/self?recent={recent}",
#         headers=user_token
#     )
#     assert response.status_code == 200

#     application = response.json()[0]["application"]

#     # delete the loan application
#     response = client.delete(
#         f"{base_url}/loan/application/{application}",
#         headers=user_token
#     )

#     # Then
#     assert response.status_code == 200
