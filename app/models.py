from sqlalchemy import Column, String, Float, Integer
from app.database import Base

class SimulatedAAPL(Base):
    __tablename__ = "simulated_aapl_live"

    timestamp = Column(String, primary_key=True, index=True)  
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

class SimulatedGOOG(Base):
    __tablename__ = "simulated_goog_live"

    timestamp = Column(String, primary_key=True, index=True)  
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

class SimulatedIBM(Base):
    __tablename__ = "simulated_ibm_live"

    timestamp = Column(String, primary_key=True, index=True)  
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

class SimulatedMSFT(Base):
    __tablename__ = "simulated_msft_live"

    timestamp = Column(String, primary_key=True, index=True)  
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

class SimulatedTSLA(Base):
    __tablename__ = "simulated_tsla_live"

    timestamp = Column(String, primary_key=True, index=True)  
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

class SimulatedUL(Base):
    __tablename__ = "simulated_ul_live"

    timestamp = Column(String, primary_key=True, index=True)  
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)


class SimulatedWMT(Base):
    __tablename__ = "simulated_wmt_live"

    timestamp = Column(String, primary_key=True, index=True)  
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Integer)



