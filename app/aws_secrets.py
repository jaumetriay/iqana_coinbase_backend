import os
import json
import boto3
from typing import Any, Dict
import logging

logger = logging.getLogger(__name__)


def get_coinbase_secrets() -> Dict[str, Any]:
    """Return the Coinbase API credentials from AWS Secrets Manager."""
    region = os.getenv("REGION", "us-east-1")
    secret_name = os.getenv("COINBASE_API_KEY", "coinbase_api_key_secret")
    profile_name = os.getenv("AWS_PROFILE", "coinbase-dev")

    try:
        session = boto3.Session(profile_name=profile_name, region_name=region)
        client = session.client("secretsmanager")

        secret_value = client.get_secret_value(SecretId=secret_name)
        secrets: Dict[str, Any] = json.loads(secret_value["SecretString"])

        logger.info("Successfully retrieved Coinbase secrets from AWS")
        return secrets

    except Exception as e:
        logger.error(f"Failed to retrieve Coinbase secrets: {e}")
        raise
