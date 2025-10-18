import os
import requests

COINBASE_API_URL = "https://api.coinbase.com/v2/accounts"

def get_holdings():
    api_key = os.getenv("COINBASE_API_KEY")
    if not api_key:
        return {"error": "Missing COINBASE_API_KEY"}

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    resp = requests.get(COINBASE_API_URL, headers=headers)
    if resp.status_code != 200:
        return {"error": f"Failed to fetch: {resp.status_code}", "body": resp.text}

    accounts = resp.json().get("data", [])
    return [
        {
            "currency": acc["balance"]["currency"],
            "amount": acc["balance"]["amount"],
            "name": acc["name"]
        }
        for acc in accounts if float(acc["balance"]["amount"]) > 0
    ]
