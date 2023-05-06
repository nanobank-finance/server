"""Tests."""
from fastapi.testclient import TestClient

from src.main import app

base_url = "http://127.0.0.1:8000"
with TestClient(app, base_url=base_url) as client:
    client = client
