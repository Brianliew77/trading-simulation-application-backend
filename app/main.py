from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from app.models import SimulatedAAPL, SimulatedGOOG, SimulatedIBM, SimulatedMSFT, SimulatedTSLA, SimulatedUL, SimulatedWMT
from app.models import GOOGHistorical, IBMHistorical, MSFTHistorical, AAPLHistorical,TSLAHistorical, ULHistorical, WMTHistorical
from app.models import CombinedAAPLData, CombinedGOOGData, CombinedIBMData, CombinedMSFTData, CombinedTSLAData, CombinedULData, CombinedWMTData
from app.models import OrderDetails
from typing import List

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
            results.append({
                "ticker": ticker,
                "last_price": row.last_price,
            })
    return results