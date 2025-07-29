from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from app.database import SessionLocal

app = FastAPI()

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
    result = db.execute(text("SELECT * FROM simulated_aapl_live LIMIT 5"))
    rows = [dict(row._mapping) for row in result]
    return rows