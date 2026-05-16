from sqlalchemy import Column, Integer, String, TIMESTAMP, func
from database.db import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(String(50), default="student")
    created_at = Column(TIMESTAMP, server_default=func.now())