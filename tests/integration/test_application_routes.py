from typing import Dict

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from src.main import app


@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
def user_token() -> Dict[str, str]:
    return {"access_token": "your_access_token"}


@pytest.mark.asyncio
async def test_submit_loan_application(client: AsyncClient, user_token: Dict[str, str]):
    # Given
    data = {"asking": 1000}

    # When
    response = await client.post("/loan/application", json=data, headers=user_token)

    # Then
    assert response.status_code == 200
    assert response.json() == {"success": True}


@pytest.mark.asyncio
async def test_get_all_loan_applications(client: AsyncClient, user_token: Dict[str, str]):
    # Given
    recent = False

    # When
    response = await client.get("/loan/application", params={"recent": recent}, headers=user_token)

    # Then
    assert response.status_code == 200
    assert "results" in response.json()


@pytest.mark.asyncio
async def test_get_my_loan_applications(client: AsyncClient, user_token: Dict[str, str]):
    # Given
    recent = False

    # When
    response = await client.get("/loan/application/user/self", params={"recent": recent}, headers=user_token)

    # Then
    assert response.status_code == 200
    assert "results" in response.json()


@pytest.mark.asyncio
async def test_get_their_loan_applications(client: AsyncClient, user_token: Dict[str, str]):
    # Given
    recent = False
    them = 123

    # When
    response = await client.get("/loan/application/user/other", params={"recent": recent, "them": them}, headers=user_token)

    # Then
    assert response.status_code == 200
    assert "results" in response.json()
