# DeFi Market Monitor

A small read-only market-data API built with FastAPI and [CCXT](https://github.com/ccxt/ccxt). It exposes a health check and a ticker endpoint that requests market data from a configurable CCXT-supported exchange.

Despite the repository name, the current implementation is an exchange ticker monitor—not an on-chain DeFi protocol analytics indexer. It does not connect to smart contracts or retrieve liquidity-pool, lending, TVL, or yield data.

## Features

- FastAPI HTTP API.
- Configurable exchange selection through `EXCHANGE_ID`.
- Market ticker retrieval through CCXT's `fetch_ticker`.
- CCXT rate limiting enabled on the exchange client.
- Read-only design: no order placement or trading methods are implemented.

## Technology

- Python
- FastAPI
- Uvicorn
- CCXT

## Requirements

- Python 3.10 or newer is recommended.
- Network access to the selected exchange's public market-data API.

## Installation

Clone the repository:

```bash
git clone https://github.com/cbt0116/defi-market-monitor.git
cd defi-market-monitor
```

Create and activate a virtual environment.

**Windows PowerShell**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configuration

The application reads the exchange identifier from the `EXCHANGE_ID` environment variable. It defaults to `binance`.

**Windows PowerShell**
```powershell
$env:EXCHANGE_ID="binance"
```

**macOS / Linux**
```bash
export EXCHANGE_ID="binance"
```

Choose an exchange identifier supported by your installed CCXT version. Exchange availability, symbols, regional restrictions, and public API behavior can vary.

## Run the API

Start the development server:

```bash
uvicorn app:app --reload
```

The local API is available at `http://127.0.0.1:8000`.

Interactive API documentation is available at `http://127.0.0.1:8000/docs`.

## Endpoints

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/health` | Returns a basic health response and indicates read-only mode |
| `GET` | `/ticker/{symbol}` | Fetches a ticker for the requested exchange market symbol |

### Health check

```http
GET /health
```

Example response:

```json
{
  "status": "ok",
  "read_only": true
}
```

### Fetch a ticker

For example, with an exchange that supports the `BTC/USDT` market:

```http
GET /ticker/BTC%2FUSDT
```

The slash in the market symbol is URL-encoded as `%2F`. The response is the ticker data returned by CCXT for the selected exchange. Available fields depend on the exchange and market.

If exchange selection or the market-data request fails, the endpoint returns HTTP 502 with a concise error category.

## How it works

- `get_exchange()` resolves the configured CCXT exchange class and creates an instance with `enableRateLimit: True`.
- `/ticker/{symbol:path}` calls the exchange's `fetch_ticker(symbol)` method.
- The application does not store ticker history or transform the exchange response into a normalized analytics model.

## Current limitations

- **Ticker only:** no order book, trades, OHLCV candles, historical analysis, or price alerts.
- **Centralized exchange data:** no direct blockchain, DEX, smart-contract, liquidity-pool, lending, or yield integrations.
- **No persistence:** ticker responses are fetched on demand and are not stored.
- **No tests included:** the repository currently has no committed automated test suite.
- **Basic error handling:** exchange errors are grouped into HTTP 502 responses; there is no retry strategy, timeout policy, or detailed operational logging.
- **No caching:** repeated requests make repeated calls to the exchange API, subject to CCXT's per-instance rate limiting.
- **No authentication or deployment hardening:** this is a minimal prototype, not a production API.

The endpoint is read-only and does not implement trading operations. Do not add exchange credentials unless a future feature genuinely requires them and handles them securely.

## Roadmap

1. Add unit tests with mocked CCXT exchange clients.
2. Validate symbols and expose clearer exchange/network error responses.
3. Add request timeouts, structured logging, and controlled retries.
4. Add optional caching to reduce repeated upstream requests.
5. Add OHLCV and order-book endpoints with documented exchange-specific behavior.
6. If expanding into DeFi analytics, add separately scoped on-chain data sources and clearly identify their provenance.
7. Add deployment configuration, monitoring, and API access controls before production use.

## Security

The current implementation uses public market-data methods and does not require API keys or trading permissions. Never commit exchange secrets, private keys, or wallet seed phrases to the repository.

## License

No license file is currently included. Unless a license is added, the repository should not be assumed to grant permission to reuse, modify, or distribute the code.
