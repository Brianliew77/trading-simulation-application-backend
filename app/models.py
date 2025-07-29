from sqlalchemy import Column, String, Float, Integer
from app.database import Base

class SimulatedAAPL(Base):
    __tablename__ = "simulated_aapl_live"

    timestamp = Column(String, primary_key=True, index=True)  # TEXT in MySQL
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
