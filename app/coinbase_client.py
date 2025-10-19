from cdp.auth.utils.jwt import generate_jwt, JwtOptions
import httpx
from typing import Dict, Any, Optional
import logging

from app.aws_secrets import get_coinbase_secrets

logger = logging.getLogger(__name__)


class CoinbaseClient:
    def __init__(self) -> None:
        self._secrets: Optional[Dict[str, Any]] = None
        self._http_client = httpx.AsyncClient(
            timeout=30.0,
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=50),
        )

    def _get_secrets(self) -> Dict[str, Any]:
        """Lazy load secrets from AWS Secrets Manager."""
        if self._secrets is None:
            self._secrets = get_coinbase_secrets()
        return self._secrets

    async def get_holdings(self) -> Dict[str, Any]:
        """Get account holdings."""
        try:
            secrets = self._get_secrets()

            jwt_token = generate_jwt(
                JwtOptions(
                    api_key_id=secrets["iqana_api_key"],
                    api_key_secret=secrets["iqana_secret"],
                    request_method="GET",
                    request_host="api.coinbase.com",
                    request_path="/api/v3/brokerage/accounts",
                    expires_in=120,
                )
            )

            response = await self._http_client.get(
                "https://api.coinbase.com/api/v3/brokerage/accounts",
                headers={"Authorization": f"Bearer {jwt_token}"},
            )

            if response.status_code == 200:
                accounts = response.json().get("accounts", [])
                holdings = [
                    {
                        "currency": acc.get("available_balance", {}).get("currency"),
                        "balance": acc.get("available_balance", {}).get("value", "0"),
                    }
                    for acc in accounts
                ]
                return {"holdings": holdings}
            else:
                return {"error": response.text}

        except Exception as e:
            logger.error(f"Error getting holdings: {e}")
            return {"error": str(e)}


coinbase_client: CoinbaseClient = CoinbaseClient()
