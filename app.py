import os
import ccxt
from fastapi import FastAPI, HTTPException

app = FastAPI(title="DeFi/CEX Market Monitor")
EXCHANGE_ID = os.getenv("EXCHANGE_ID", "binance")

def get_exchange():
    exchange_cls = getattr(ccxt, EXCHANGE_ID, None)
    if exchange_cls is None:
        raise ValueError("Unsupported exchange")
    return exchange_cls({"enableRateLimit": True})

@app.get("/health")
def health():
    return {"status": "ok", "read_only": True}

@app.get("/ticker/{symbol:path}")
def ticker(symbol: str):
    try:
        exchange = get_exchange()
        return exchange.fetch_ticker(symbol)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Market data unavailable: {type(exc).__name__}")
