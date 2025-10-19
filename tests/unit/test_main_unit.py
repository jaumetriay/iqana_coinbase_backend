from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_health() -> None:
    """Test health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200


def test_root() -> None:
    """Test root endpoint."""
    response = client.get("/")
    assert response.status_code == 200


@patch("app.main.coinbase_client.get_holdings")
def test_holdings_success(mock_get: MagicMock) -> None:
    """Test holdings endpoint."""
    mock_get.return_value = {"holdings": []}
    response = client.get("/holdings")
    assert response.status_code == 200
