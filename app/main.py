from fastapi import FastAPI
from app.coinbase_client import get_holdings

app = FastAPI()

@app.get("/holdings")
def holdings():
    data = get_holdings()
    return {"holdings": data}
