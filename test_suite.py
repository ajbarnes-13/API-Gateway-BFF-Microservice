# Test suite for main.py in API-Gateway-BFF-Microservice.
# Date: 9/26/26
# Tests written by Gemini AI

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, AsyncMock, MagicMock

from main import app

client = TestClient(app)

def test_start_service():
    """
    Tests the root health check endpoint.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == ["API Service is Running..."]

@patch("main.httpx.AsyncClient")
def test_gateway_invalid_route(mock_client):
    """
    Tests that the Gateway correctly rejects unknown APIs.
    """
    response = client.get("/unknown_api")
    assert response.status_code == 200
    assert response.json() == {"Error": "'unknown_api' not found in API Dictionary."}

@patch("main.httpx.AsyncClient")
def test_gateway_valid_route(mock_httpx_client):
    """
    Tests the Gateway successfully forwards a request.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {"fact": "Cats sleep 70% of their lives."}

    mock_instance = mock_httpx_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.request = AsyncMock(return_value=mock_response)

    response = client.get("/catfacts")

    assert response.status_code == 200
    assert response.json() == {"fact": "Cats sleep 70% of their lives."}


@patch("main.httpx.AsyncClient")
def test_aggregator(mock_httpx_client):
    """
    Tests the BFF Aggregator looping through a dictionary payload.
    """
    mock_response = MagicMock()
    mock_response.json.return_value = {"fact": "Mocked cat fact"}

    mock_instance = mock_httpx_client.return_value
    mock_instance.__aenter__.return_value = mock_instance
    mock_instance.get = AsyncMock(return_value=mock_response)

    payload = {
        "catfacts": {"limit": 1}
    }

    response = client.post("/aggregate", json=payload)

    assert response.status_code == 200
    assert response.json() == {"catfacts": {"fact": "Mocked cat fact"}}
