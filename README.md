# Trading Simulation — Backend (FastAPI + MySQL)

FastAPI service that serves market snapshots, candlestick data, orders, account balances, and curated news for a local paper‑trading simulation.

## Tech stack
- FastAPI, Pydantic
- SQLAlchemy ORM
- MySQL (via `mysql-connector-python`)
- Uvicorn (ASGI)
- CORS configured for React dev server (`http://localhost:3000`)

## Project layout
```
app/
  main.py          # FastAPI routes
  database.py      # SQLAlchemy engine/session (configure credentials here)
  models.py        # ORM models (tables for combined_* data, orders, accounts, news)
requirements.txt
```

## Prerequisites
- Python 3.10+
- MySQL 8.x
- A database named `stocks` populated with the expected tables:
  - `combined_aapl_data`, `combined_goog_data`, `combined_ibm_data`, `combined_msft_data`, `combined_tsla_data`, `combined_ul_data`, `combined_wmt_data`
  - `order_details`, `account_details`
  - `stock_news_summary`
  - (Optionally) `simulated_*_live` tables if you plan to extend live views

> **Tip:** The service reads from `combined_*` tables for historical candles and last prices, and from `order_details` / `account_details` for portfolio/account views.

## Setup

1) **Create & configure MySQL**
```sql
-- Example: create the schema
CREATE DATABASE IF NOT EXISTS stocks;
USE stocks;

-- Minimal structures (adapt to your data loader)
-- combined_* tables (excerpt of common fields)
-- timestamp (PK), timestamp_date, timestamp_time, hist_open, hist_high, hist_low, adjusted_close, last_price, volume_curr_price, vol_rolling_average, low_rolling_average, high_rolling_average, etc.

-- Orders & account
CREATE TABLE IF NOT EXISTS account_details (
  account_number INT PRIMARY KEY,
  cash_total DECIMAL(15,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS order_details (
  id INT AUTO_INCREMENT PRIMARY KEY,
  account_number INT NOT NULL,
  ticker VARCHAR(10) NOT NULL,
  action VARCHAR(10) NOT NULL,         -- BUY / SELL
  trade_type VARCHAR(10) NOT NULL,     -- LIMIT / MARKET
  quantity INT NOT NULL,
  quantity_filled INT NOT NULL DEFAULT 0,
  price DOUBLE NOT NULL,
  status TEXT NOT NULL,                -- e.g., FILLED / QUEUED / CANCELLED
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- News
CREATE TABLE IF NOT EXISTS stock_news_summary (
  id INT AUTO_INCREMENT PRIMARY KEY,
  headline TEXT NOT NULL,
  timestamp_human TEXT,
  topic_tags TEXT,
  ticker_1_label TEXT
);
```

2) **Configure database credentials**
Open `app/database.py` and set:
```python
SQL_USERNAME = "root"
SQL_PASSWORD = "your_password"
SQL_HOST = "localhost"
SQL_PORT = "3306"
SQL_DATABASE = "stocks"
```
> Optional: refactor to read from environment variables. If you do, consider
`SQL_USERNAME`, `SQL_PASSWORD`, `SQL_HOST`, `SQL_PORT`, `SQL_DATABASE`.

3) **Install dependencies**
> `requirements.txt` may be saved in UTF‑16. If `pip install -r requirements.txt`
errors on encoding, re‑save the file as UTF‑8 or run:
```bash
python - <<'PY'
import codecs, shutil, sys
src = "requirements.txt"; dst = "requirements-utf8.txt"
codecs.open(dst, "w", "utf-8").write(codecs.open(src, "r", "utf-16").read())
print("Wrote", dst)
PY

pip install -r requirements-utf8.txt
```
(Or just `pip install fastapi uvicorn sqlalchemy mysql-connector-python python-dotenv` for a minimal run.)

4) **Run the API**
```bash
uvicorn app.main:app --reload --port 8000
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

## CORS
`main.py` allows `http://localhost:3000` by default:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Endpoints

- `GET /ping-db` → quick DB connectivity check.
- `GET /timestamps` → distinct timestamps (uses AAPL combined table as reference).
- `GET /trading-data?timestamp=YYYY-MM-DD HH:MM:SS` → snapshot of OHLC/volume‑style fields per ticker for a timestamp.
- `GET /order-details?timestamp=...` → order list (optionally filtered by timestamp).
- `GET /account-details` → account number and cash balance (includes realized P/L aggregation).
- `GET /trading-last-price?timestamp=...` → per‑ticker: last price, quantity owned, average buy, unrealized P/L.
- `POST /orders` → place an order (body below).
- `GET /api/market-info?ticker=...&search=...&order=asc|desc&order_by=id|timestamp_human` → news items with totals.
- `GET /candles?ticker=AAPL|GOOG|IBM|MSFT|TSLA|UL|WMT&upto=YYYY-MM-DD HH:MM:SS&limit=120` → lightweight‑charts formatted candles (epoch seconds + OHLC).

### `POST /orders` body (example)
```json
{
  "ticker": "AAPL",
  "action": "BUY",
  "price": 199.5,
  "quantity": 10,
  "trade_type": "LIMIT"   // or "MARKET"
}
```

### Notes on data assumptions
- Combined tables expose both historical (`hist_open`, `hist_high`, `hist_low`, `adjusted_close`) and rolling stats (`high_min`, `low_min`, `vol_rolling_average`, etc.) plus a `last_price` used for snapshots and P/L.
- Portfolio calculations aggregate `order_details` for a fixed account number configured in code.
  - In `main.py` the placeholder is `BRIAN_ACC_NUM`. Update it or extend auth later.
- For charts, `/candles` returns oldest→newest order with `{time, open, high, low, close}`.

## Running with Docker (optional snippet)
```dockerfile
# Dockerfile (example)
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt ./
# If requirements.txt is UTF-16, convert to UTF-8 first or use a minimal list
RUN pip install --no-cache-dir -r requirements.txt || true
COPY app ./app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting
- **`pymysql.err.OperationalError` / connection refused**: verify host/port/user/pass; ensure MySQL is running and DB exists.
- **Empty responses**: confirm the `combined_*` tables contain rows for the timestamps your frontend requests.
- **CORS errors**: add your frontend origin to `allow_origins`.
