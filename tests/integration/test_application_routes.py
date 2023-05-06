from typing import Dict

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)
base_url = "http://127.0.0.1:8000"


@pytest.fixture()
def client():
    with TestClient(app, base_url=base_url) as client:
        yield client


@pytest.fixture
def user_token() -> Dict[str, str]:
    return {"access_token": "your_access_token"}


def test_submit_loan_application(user_token, client):
    # Given
    asking = 1000

    # When
    response = client.post(f"{base_url}/loan/application?asking={asking}", headers=user_token)

    # Then
    print(response.__dict__)
    assert response.status_code == 200
    assert response.json()["success"] == True


# @pytest.mark.asyncio
# async def test_get_all_loan_applications(client: AsyncClient, user_token: Dict[str, str]):
#     # Given
#     recent = False

#     # When
#     response = await client.get(f"{base_url}/loan/application", params={"recent": recent}, headers=user_token)

#     # Then
#     assert response.status_code == 200
#     assert "results" in response.json()


# @pytest.mark.asyncio
# async def test_get_my_loan_applications(client: AsyncClient, user_token: Dict[str, str]):
#     # Given
#     recent = False

#     # When
#     response = await client.get(f"{base_url}/loan/application/user/self", params={"recent": recent}, headers=user_token)

#     # Then
#     assert response.status_code == 200
#     assert "results" in response.json()


# @pytest.mark.asyncio
# async def test_get_their_loan_applications(client: AsyncClient, user_token: Dict[str, str]):
#     # Given
#     recent = False
#     them = 123

#     # When
#     response = await client.get(f"{base_url}/loan/application/user/other", params={"recent": recent, "them": them}, headers=user_token)

#     # Then
#     assert response.status_code == 200
#     assert "results" in response.json()


# @pytest.mark.asyncio
# async def test_withdraw_loan_application(client: AsyncClient, user_token: Dict[str, str]):
#     # Create an application
#     response = await client.post(f"{base_url}/loan/application", json={"asking": 1000}, headers=user_token)
#     # Get the application
#     response = await client.get(f"{base_url}/loan/application/user/self", params={"recent": True}, headers=user_token)
#     # Parse the results, get the application id to withdraw
#     print(response.json())
#     application = response.json()
#     # Withdraw the application
#     response = await client.delete(f"{base_url}/loan/application/{application}", headers=user_token)

#     # Then
#     assert response.status_code == 200
#     assert response.json()["success"] is True
