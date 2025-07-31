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


class CombinedAAPLData(Base):
    __tablename__ = "combined_aapl_data"

    timestamp = Column(String, primary_key=True, index=True)
    timestamp_date = Column(String)
    timestamp_time = Column(String)
    live_open = Column(Float)
    high_min = Column(Float)
    low_min = Column(Float)
    live_close = Column(Float)
    volume_curr_price = Column(Integer)
    hist_open = Column(Float)
    hist_high = Column(Float)
    hist_low = Column(Float)
    hist_close = Column(Float)
    adjusted_close = Column(Float)
    hist_volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)
    vol_rolling_average = Column(Float)

class CombinedGOOGData(Base):
    __tablename__ = "combined_goog_data"
    # Same schema as above
    timestamp = Column(String, primary_key=True, index=True)
    timestamp_date = Column(String)
    timestamp_time = Column(String)
    live_open = Column(Float)
    high_min = Column(Float)
    low_min = Column(Float)
    live_close = Column(Float)
    volume_curr_price = Column(Integer)
    hist_open = Column(Float)
    hist_high = Column(Float)
    hist_low = Column(Float)
    hist_close = Column(Float)
    adjusted_close = Column(Float)
    hist_volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)
    vol_rolling_average = Column(Float)

class CombinedIBMData(Base):
    __tablename__ = "combined_ibm_data"
    # Repeat same fields as above
    timestamp = Column(String, primary_key=True, index=True)
    timestamp_date = Column(String)
    timestamp_time = Column(String)
    live_open = Column(Float)
    high_min = Column(Float)
    low_min = Column(Float)
    live_close = Column(Float)
    volume_curr_price = Column(Integer)
    hist_open = Column(Float)
    hist_high = Column(Float)
    hist_low = Column(Float)
    hist_close = Column(Float)
    adjusted_close = Column(Float)
    hist_volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)
    vol_rolling_average = Column(Float)

class CombinedMSFTData(Base):
    __tablename__ = "combined_msft_data"
    # Repeat same fields
    timestamp = Column(String, primary_key=True, index=True)
    timestamp_date = Column(String)
    timestamp_time = Column(String)
    live_open = Column(Float)
    high_min = Column(Float)
    low_min = Column(Float)
    live_close = Column(Float)
    volume_curr_price = Column(Integer)
    hist_open = Column(Float)
    hist_high = Column(Float)
    hist_low = Column(Float)
    hist_close = Column(Float)
    adjusted_close = Column(Float)
    hist_volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)
    vol_rolling_average = Column(Float)

class CombinedTSLAData(Base):
    __tablename__ = "combined_tsla_data"
    # Repeat same fields
    timestamp = Column(String, primary_key=True, index=True)
    timestamp_date = Column(String)
    timestamp_time = Column(String)
    live_open = Column(Float)
    high_min = Column(Float)
    low_min = Column(Float)
    live_close = Column(Float)
    volume_curr_price = Column(Integer)
    hist_open = Column(Float)
    hist_high = Column(Float)
    hist_low = Column(Float)
    hist_close = Column(Float)
    adjusted_close = Column(Float)
    hist_volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)
    vol_rolling_average = Column(Float)

class CombinedULData(Base):
    __tablename__ = "combined_ul_data"
    # Repeat same fields
    timestamp = Column(String, primary_key=True, index=True)
    timestamp_date = Column(String)
    timestamp_time = Column(String)
    live_open = Column(Float)
    high_min = Column(Float)
    low_min = Column(Float)
    live_close = Column(Float)
    volume_curr_price = Column(Integer)
    hist_open = Column(Float)
    hist_high = Column(Float)
    hist_low = Column(Float)
    hist_close = Column(Float)
    adjusted_close = Column(Float)
    hist_volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)
    vol_rolling_average = Column(Float)

class CombinedWMTData(Base):
    __tablename__ = "combined_wmt_data"
    # Repeat same fields
    timestamp = Column(String, primary_key=True, index=True)
    timestamp_date = Column(String)
    timestamp_time = Column(String)
    live_open = Column(Float)
    high_min = Column(Float)
    low_min = Column(Float)
    live_close = Column(Float)
    volume_curr_price = Column(Integer)
    hist_open = Column(Float)
    hist_high = Column(Float)
    hist_low = Column(Float)
    hist_close = Column(Float)
    adjusted_close = Column(Float)
    hist_volume = Column(Integer)
    dividend_amount = Column(Float)
    split_coefficient = Column(Float)
    vol_rolling_average = Column(Float)
