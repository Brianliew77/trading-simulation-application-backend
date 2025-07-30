from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from app.models import SimulatedAAPL, SimulatedGOOG, SimulatedIBM, SimulatedMSFT, SimulatedTSLA, SimulatedUL, SimulatedWMT
from app.models import GOOGHistorical, IBMHistorical, MSFTHistorical, AAPLHistorical,TSLAHistorical, ULHistorical, WMTHistorical
from typing import List

app = FastAPI()

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


@app.get("/stocks")
def get_stocks(db: Session = Depends(get_db)):
    result = {
        # Live data
        "aapl_live": db.query(SimulatedAAPL).limit(2).all(),
        "goog_live": db.query(SimulatedGOOG).limit(2).all(),
        "ibm_live": db.query(SimulatedIBM).limit(2).all(),
        "msft_live": db.query(SimulatedMSFT).limit(2).all(),
        "tsla_live": db.query(SimulatedTSLA).limit(2).all(),
        "ul_live": db.query(SimulatedUL).limit(2).all(),
        "wmt_live": db.query(SimulatedWMT).limit(2).all(),

        # Historical data
        "aapl_hist": db.query(AAPLHistorical).limit(2).all(),
        "goog_hist": db.query(GOOGHistorical).limit(2).all(),
        "ibm_hist": db.query(IBMHistorical).limit(2).all(),
        "msft_hist": db.query(MSFTHistorical).limit(2).all(),
        "tsla_hist": db.query(TSLAHistorical).limit(2).all(),
        "ul_hist": db.query(ULHistorical).limit(2).all(),
        "wmt_hist": db.query(WMTHistorical).limit(2).all(),
    }
    return result