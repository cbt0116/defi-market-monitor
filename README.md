# DeFi Market Monitor

Read-only market data endpoint backed by CCXT. Example:
```bash
pip install -r requirements.txt
uvicorn app:app --reload
# GET http://127.0.0.1:8000/ticker/BTC%2FUSDT
```
Set `EXCHANGE_ID` to an exchange supported by CCXT. Exchange symbols and API availability vary. No trading methods or credentials are used.
