import pytest
from unittest.mock import patch, MagicMock
from app.coinbase_client import CoinbaseClient


@pytest.mark.asyncio  # type: ignore[misc]
async def test_get_holdings_success() -> None:
    """Test successful holdings retrieval."""
    client = CoinbaseClient()

    with patch("app.coinbase_client.get_coinbase_secrets") as mock_secrets:
        mock_secrets.return_value = {"iqana_api_key": "test", "iqana_secret": "test"}

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"accounts": []}

        with patch.object(client._http_client, "get", return_value=mock_response):
            result = await client.get_holdings()
            assert "holdings" in result


@pytest.mark.asyncio  # type: ignore[misc]
async def test_get_holdings_error() -> None:
    """Test API error."""
    client = CoinbaseClient()

    with patch("app.coinbase_client.get_coinbase_secrets") as mock_secrets:
        mock_secrets.return_value = {"iqana_api_key": "test", "iqana_secret": "test"}

        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"

        with patch.object(client._http_client, "get", return_value=mock_response):
            result = await client.get_holdings()
            assert "error" in result
