from sqlalchemy import Column, Integer, String
from database.db import Base

class User(Base):
    __tablename__ = "users"

    # Map the Python attribute to the database column name exactly
    id = Column("user_id", Integer, primary_key=True, index=True)
    fullname = Column("full_name", String(100))
    email = Column(String(100), unique=True)
    password = Column("password_hash", String(255))