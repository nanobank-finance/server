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
