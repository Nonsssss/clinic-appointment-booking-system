from sqlalchemy import Column, Integer, String
from database.db import Base

class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String(100))
    specialization = Column(String(100))