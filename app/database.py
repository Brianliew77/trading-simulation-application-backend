from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ✅ Replace with your actual credentials
SQL_USERNAME = "root"
SQL_PASSWORD = "brian18"  # your MySQL password, leave "" if no password
SQL_HOST = "localhost"
SQL_PORT = "3306"
SQL_DATABASE = "stocks"

# MySQL SQLAlchemy connection string
SQLALCHEMY_DATABASE_URL = (
    f"mysql+mysqlconnector://{SQL_USERNAME}:{SQL_PASSWORD}@{SQL_HOST}:{SQL_PORT}/{SQL_DATABASE}"
)

# SQLAlchemy engine/session setup
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
