from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session, load_only
from sqlalchemy import text, and_, select, func
from app.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from app.models import SimulatedAAPL, SimulatedGOOG, SimulatedIBM, SimulatedMSFT, SimulatedTSLA, SimulatedUL, SimulatedWMT
from app.models import GOOGHistorical, IBMHistorical, MSFTHistorical, AAPLHistorical,TSLAHistorical, ULHistorical, WMTHistorical
from app.models import CombinedAAPLData, CombinedGOOGData, CombinedIBMData, CombinedMSFTData, CombinedTSLAData, CombinedULData, CombinedWMTData
from app.models import OrderDetails, StockNewsSummary
from typing import List, Literal, Optional, Union, Tuple
from pydantic import BaseModel, Field
from datetime import datetime, date, time as dtime, timezone, timedelta

app = FastAPI()

BRIAN_ACC_NUM = 219771

# 👇 Allow your React frontend to access the FastAPI backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class OrderCreate(BaseModel):
    ticker: str
    action: Literal["BUY", "SELL"]
    price: float = Field(gt=0)
    quantity: int = Field(gt=0)
    trade_type: Literal["LIMIT", "MARKET"]
    datetime: str                       # "YYYY-MM-DD HH:MM:SS"
    account_number: int = BRIAN_ACC_NUM

class NewsItem(BaseModel):
    headline: str
    timestamp_human: str | None = None
    topic_tags: str | None = None
    ticker_1: str | None = None

class NewsResponse(BaseModel):
    total: int
    items: List[NewsItem]

@app.get("/ping-db")
def ping_db(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "Database connection successful"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

@app.get("/timestamps", response_model=List[str])
def get_timestamps(db: Session = Depends(get_db)):
    # Using AAPL table as reference
    rows = db.query(CombinedAAPLData.timestamp).distinct().all()
    return [row[0] for row in rows]

@app.get("/trading-data")
def get_trading_data(timestamp: str, db: Session = Depends(get_db)):
    tickers = [
        ("AAPL", CombinedAAPLData),
        ("GOOG", CombinedGOOGData),
        ("IBM", CombinedIBMData),
        ("MSFT", CombinedMSFTData),
        ("TSLA", CombinedTSLAData),
        ("UL", CombinedULData),
        ("WMT", CombinedWMTData),
    ]

    results = []
    for ticker, model in tickers:
        row = db.query(model).filter(model.timestamp == timestamp).first()
        if row:
            results.append({
                "ticker": ticker,
                "high": row.high_min,
                "low": row.low_min,
                "last_price": row.last_price,
                "volume_curr_price": row.volume_curr_price,
                "open": row.hist_open,
                "todays_high": row.high_rolling_average,
                "todays_low": row.low_rolling_average,
                "close": row.hist_close,
                "hist_volume": row.vol_rolling_average
            })
    return results


@app.get("/order-details")
def get_order_details(db: Session = Depends(get_db)):
    orders = db.query(OrderDetails).all()
    return [
        {
            "id": order.id,
            "ticker": order.ticker,
            "quantity": order.quantity,
            "action": order.action,
            "portfolio_balance_change": float(order.portfolio_balance_change),
            "datetime": order.datetime,
            "trade_type": order.trade_type,
            "account_number": order.account_number,
            "status": order.status,
            "quantity_filled": order.quantity_filled,
            "price": order.price
        }
        for order in orders
    ]



@app.get("/account-details")
def get_account_details(db: Session = Depends(get_db)):
    account_number = BRIAN_ACC_NUM # fixed for now
    result = db.execute(text(f"SELECT * FROM account_details WHERE account_number = {account_number}")).fetchone()
    orders = db.query(OrderDetails).filter(OrderDetails.account_number == account_number).all()
    sum_count = 0
    for order in orders:
        if order.portfolio_balance_change is not None:
            sum_count += order.portfolio_balance_change
    if result:
        return {
            "account_number": result[0],
            "cash_total": float(result[1]) + float(sum_count)
        }
    return {"error": "Account not found"}



@app.get("/trading-last-price")
def get_trading_last_price(timestamp: str, db: Session = Depends(get_db)):
    tickers = [
        ("AAPL", CombinedAAPLData),
        ("GOOG", CombinedGOOGData),
        ("IBM", CombinedIBMData),
        ("MSFT", CombinedMSFTData),
        ("TSLA", CombinedTSLAData),
        ("UL", CombinedULData),
        ("WMT", CombinedWMTData),
    ]

    results = []
    for ticker, model in tickers:
        row = db.query(model).filter(model.timestamp == timestamp).first()
        
        if row:
            # Fetch all relevant orders
            orders = db.query(OrderDetails).filter(
                and_(
                    OrderDetails.ticker == ticker,
                    OrderDetails.account_number == BRIAN_ACC_NUM,
                    OrderDetails.action == "BUY",
                    OrderDetails.status.in_(["FILLED", "PARTIALLY FILLED"])
                )
            ).all()

            total_qty = 0
            total_cost = 0.0
            for order in orders:
                try:
                    qty = int(order.quantity_filled)
                    price = order.price or 0.0
                    total_qty += qty
                    total_cost += qty * price
                except:
                    continue

            average_price = (total_cost / total_qty) if total_qty > 0 else 0.0

            profits = (row.last_price - average_price) * total_qty
            results.append({
                "ticker": ticker,
                "last_price": row.last_price,
                "quantity_owned": total_qty,
                "average_buy_price": round(average_price, 4),
                "profit": round(profits,2)
            })

    return results

@app.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # normalize
    ticker = order.ticker.upper().strip()
    action = order.action.upper().strip()
    trade_type = order.trade_type.upper().strip()

    # 1) quantity_filled & status
    if trade_type == "MARKET":
        quantity_filled = order.quantity
        status = "FILLED"
    else:  # LIMIT
        # 50% filled rule
        quantity_filled = int(round(order.quantity * 0.5))
        status = "PARTIALLY FILLED"

    # 2) portfolio_balance_change
    # BUY = outflow (negative), SELL = inflow (positive)
    sign = -1 if action == "BUY" else 1
    portfolio_change = sign * (order.price * quantity_filled)

    # 3) insert
    row = OrderDetails(
        ticker=ticker,
        quantity=order.quantity,
        action=action,
        portfolio_balance_change=portfolio_change,
        datetime=order.datetime,      # stored as text in your table
        trade_type=trade_type,
        account_number=order.account_number,
        status=status,
        quantity_filled=quantity_filled,
        price=order.price,
    )

    db.add(row)
    db.commit()
    db.refresh(row)

    return {
        "id": row.id,
        "message": "Order recorded",
        "saved": {
            "ticker": row.ticker,
            "action": row.action,
            "trade_type": row.trade_type,
            "quantity": row.quantity,
            "quantity_filled": row.quantity_filled,
            "price": row.price,
            "datetime": row.datetime,
            "account_number": row.account_number,
            "status": row.status,
            "portfolio_balance_change": float(row.portfolio_balance_change),
        },
    }

def fetch_market_info(
    db: Session,
    *,
    ticker: Optional[str] = None,
    search: Optional[str] = None,
    order: Literal["asc", "desc"] = "asc",  # default to id ascending for 1..20
    order_by: Literal["id", "timestamp_human"] = "id",
) -> List[StockNewsSummary]:
    """
    Return rows where id is between 1 and 20 (inclusive).
    Deterministic ordering via `order_by` (defaults to id).
    """
    stmt = select(StockNewsSummary).options(
        load_only(
            StockNewsSummary.headline,
            StockNewsSummary.timestamp_human,
            StockNewsSummary.topic_tags,
            StockNewsSummary.ticker_1,
        )
    )

    # Restrict to id 1..20
    if not hasattr(StockNewsSummary, "id"):
        raise ValueError("StockNewsSummary.id is required to filter id=1..20.")
    stmt = stmt.where(StockNewsSummary.id.between(1, 20))

    if ticker:
        stmt = stmt.where(StockNewsSummary.ticker_1 == ticker)

    if search:
        stmt = stmt.where(StockNewsSummary.headline.ilike(f"%{search}%"))

    # Choose order column; default to id
    order_col = getattr(StockNewsSummary, order_by, None) or StockNewsSummary.id

    if order == "asc":
        stmt = stmt.order_by(order_col.asc())
        # stable tie-breaker
        if order_col is not StockNewsSummary.id:
            stmt = stmt.order_by(order_col.asc(), StockNewsSummary.id.asc())
    else:
        stmt = stmt.order_by(order_col.desc())
        if order_col is not StockNewsSummary.id:
            stmt = stmt.order_by(order_col.desc(), StockNewsSummary.id.desc())

    rows = db.execute(stmt).scalars().all()
    return rows


@app.get("/api/market-info", response_model=NewsResponse)
def get_market_info(
    ticker: Optional[str] = Query(None, description="Filter by ticker_1"),
    search: Optional[str] = Query(None, description="Search in headline"),
    order: Literal["asc", "desc"] = "asc",  # default to id ascending for 1..20
    order_by: Literal["id", "timestamp_human"] = "id",
    db: Session = Depends(get_db),
):
    rows = fetch_market_info(
        db,
        ticker=ticker,
        search=search,
        order=order,
        order_by=order_by,
    )
    return {
        "total": len(rows),
        "items": [
            NewsItem(
                headline=r.headline,
                timestamp_human=r.timestamp_human,
                topic_tags=r.topic_tags,
                ticker_1=r.ticker_1,
            )
            for r in rows
        ],
    }

def to_utc_ts(d: date, t: dtime | None) -> int:
    """
    Combine date + time to a UTC epoch seconds int.
    If time is None, default to 00:00:00.
    """
    if t is None:
        t = dtime(0, 0, 0)
    dt = datetime.combine(d, t).replace(tzinfo=timezone.utc)
    return int(dt.timestamp())

def _to_time(val: Optional[Union[dtime, timedelta, str]]) -> Optional[dtime]:
    """
    Normalize DB time column to datetime.time.
    - timedelta -> (datetime.min + val).time()
    - 'HH:MM[:SS]' -> parsed time
    - None -> None
    """
    if val is None:
        return None
    if isinstance(val, dtime):
        return val
    if isinstance(val, timedelta):
        # timedelta since midnight
        return (datetime.min + val).time()
    if isinstance(val, str):
        # be forgiving: 'HH:MM' or 'HH:MM:SS'
        try:
            fmt = "%H:%M:%S" if val.count(":") == 2 else "%H:%M"
            return datetime.strptime(val, fmt).time()
        except Exception:
            return None
    return None

def _to_utc_epoch(ts_date: date, ts_time: Optional[dtime]) -> int:
    if ts_time is None:
        ts_time = dtime(0, 0, 0)
    dt = datetime.combine(ts_date, ts_time).replace(tzinfo=timezone.utc)
    return int(dt.timestamp())

# ---- endpoint -------------------------------------------------------------

TICKER_TO_MODEL = {
    "AAPL": CombinedAAPLData,
    "GOOG": CombinedGOOGData,
    "IBM":  CombinedIBMData,
    "MSFT": CombinedMSFTData,
    "TSLA": CombinedTSLAData,
    "UL":   CombinedULData,
    "WMT":  CombinedWMTData,
}

@app.get("/candles")
def get_candles(
    ticker: Literal["AAPL", "GOOG", "IBM", "MSFT", "TSLA", "UL", "WMT"],
    upto: str,                    # same format as Combined*.timestamp, e.g. "YYYY-MM-DD HH:MM:SS"
    limit: int = 120,
    db: Session = Depends(get_db),
):
    Model = TICKER_TO_MODEL[ticker]

    # newest -> oldest (so we can limit), then reverse
    rows = (
        db.query(
            Model.timestamp_date,
            Model.timestamp_time,
            Model.hist_open.label("open"),
            Model.hist_high.label("high"),
            Model.hist_low.label("low"),
            Model.adjusted_close.label("close"),
        )
        .filter(Model.timestamp <= upto)
        .order_by(Model.timestamp_date.desc(), Model.timestamp_time.desc())
        .limit(limit)
        .all()
    )

    if not rows:
        return []

    rows = list(reversed(rows))  # oldest -> newest for the chart

    candles = []
    for r in rows:
        ts_time = _to_time(r[1])
        epoch = _to_utc_epoch(r[0], ts_time)
        candles.append({
            "time": epoch,
            "open": float(r.open) if r.open is not None else None,
            "high": float(r.high) if r.high is not None else None,
            "low":  float(r.low)  if r.low  is not None else None,
            "close": float(r.close) if r.close is not None else None,
        })

    return candles