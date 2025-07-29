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


class GOOGHistorical(Base):
    __tablename__ = "goog_2025_historical"

    timestamp = Column(String, primary_key=True, index=True) 
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)

class IBMHistorical(Base):
    __tablename__ = "ibm_2025_historical"

    timestamp = Column(String, primary_key=True, index=True) 
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)


class MSFTHistorical(Base):
    __tablename__ = "msft_2025_historical"

    timestamp = Column(String, primary_key=True, index=True) 
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)

class AAPLHistorical(Base):
    __tablename__ = "simulated_aapl_2025_historical"

    timestamp = Column(String, primary_key=True, index=True) 
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)

class TSLAHistorical(Base):
    __tablename__ = "tsla_2025_historical"

    timestamp = Column(String, primary_key=True, index=True) 
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)

class ULHistorical(Base):
    __tablename__ = "ul_2025_historical"

    timestamp = Column(String, primary_key=True, index=True) 
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)

class WMTHistorical(Base):
    __tablename__ = "wmt_2025_historical"

    timestamp = Column(String, primary_key=True, index=True) 
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    adjusted_close = Column(Float)
    volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)