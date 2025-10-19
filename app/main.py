from fastapi import FastAPI
from typing import Any, Dict
import logging

from app.coinbase_client import coinbase_client

logger = logging.getLogger(__name__)

app = FastAPI(
    title="Coinbase Holdings API",
    version="0.1.0",
    description="API to retrieve Coinbase account holdings",
)


@app.get("/holdings", response_model=Dict[str, Any])
async def holdings() -> Dict[str, Any]:
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
