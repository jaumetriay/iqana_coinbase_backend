from fastapi import FastAPI, Request
from typing import Any, Dict
import logging
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.coinbase_client import coinbase_client

logger = logging.getLogger(__name__)
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Coinbase Holdings API",
    version="0.1.0",
    description="API to retrieve Coinbase account holdings",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/holdings", response_model=Dict[str, Any])
@limiter.limit("10/minute")
async def holdings(request: Request) -> Dict[str, Any]:
    """Get Coinbase account holdings."""
    try:
        result = await coinbase_client.get_holdings()

        if "holdings" in result:
            return {
                "success": True,
                "data": result["holdings"],
                "count": len(result["holdings"]),
            }
        else:
            return {"success": False, "error": result.get("error", "Unknown error")}

    except Exception as e:
        logger.error(f"Unexpected error in holdings endpoint: {e}", exc_info=True)
        return {"success": False, "error": "Internal server error", "details": str(e)}


@app.get("/health", response_model=Dict[str, str])
async def health_check() -> Dict[str, str]:
    return {"status": "healthy", "service": "coinbase-holdings-api"}


@app.get("/", response_model=Dict[str, Any])
async def root() -> Dict[str, Any]:
    return {"message": "Coinbase Holdings API", "endpoints": ["/holdings", "/health"]}
