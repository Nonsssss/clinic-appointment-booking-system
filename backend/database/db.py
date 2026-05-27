import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()  # loads .env if present, ignored if not

DB_USER = os.environ.get("MYSQLUSER") or os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("MYSQLPASSWORD") or os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("MYSQLHOST") or os.environ.get("DB_HOST", "127.0.0.1")
DB_PORT = os.environ.get("MYSQLPORT") or os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("MYSQLDATABASE") or os.environ.get("DB_NAME")

# Fail fast with a clear message if any required var is missing
missing = [k for k, v in {
    "MYSQLUSER": DB_USER,
    "MYSQLPASSWORD": DB_PASSWORD,
    "MYSQLHOST": DB_HOST,
    "MYSQLDATABASE": DB_NAME,
}.items() if not v]

if missing:
    raise RuntimeError(f"Missing required database env vars: {', '.join(missing)}")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

print(f"Connecting to database host: {DB_HOST}")

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()