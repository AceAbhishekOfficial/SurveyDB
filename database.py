import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Prefer a full DATABASE_URL env var; otherwise build from parts.
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    DB_USER = os.getenv("DB_USER", "admin")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "Awkc7fcrJFGbPAkbnnIm")
    DB_HOST = os.getenv("DB_HOST", "database-1.cluqwyq6oawx.eu-north-1.rds.amazonaws.com")
    DB_PORT = os.getenv("DB_PORT", "3306")
    DB_NAME = os.getenv("DB_NAME", "village_db")
    DB_DRIVER = os.getenv("DB_DRIVER", "mysql+pymysql")
    DB_PASSWORD_Q = quote_plus(DB_PASSWORD)
    DATABASE_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD_Q}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
