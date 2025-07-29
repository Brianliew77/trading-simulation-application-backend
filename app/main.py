from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal
from fastapi.middleware.cors import CORSMiddleware
from app.models import SimulatedAAPL, SimulatedGOOG, SimulatedIBM, SimulatedMSFT, SimulatedTSLA, SimulatedUL, SimulatedWMT
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
        "aapl": db.query(SimulatedAAPL).limit(2).all(),
        "goog": db.query(SimulatedGOOG).limit(2).all(),
        "ibm": db.query(SimulatedIBM).limit(2).all(),
        "msft": db.query(SimulatedMSFT).limit(2).all(),
        "tsla": db.query(SimulatedTSLA).limit(2).all(),
        "ul": db.query(SimulatedUL).limit(2).all(),
        "wmt": db.query(SimulatedWMT).limit(2).all(),
    }
    return result
