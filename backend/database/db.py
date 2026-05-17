import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv 


load_dotenv()

DATABASE_URL = (
    
    f"mysql+pymysql://{os.getenv('MYSQLUSER')}:"
    f"{os.getenv('MYSQLPASSWORD')}@"
    f"{os.getenv('MYSQLHOST')}/"
    f"{os.getenv('MYSQLDATABASE')}"
)
  


engine = create_engine(
    DATABASE_URL, 
    echo=True 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()