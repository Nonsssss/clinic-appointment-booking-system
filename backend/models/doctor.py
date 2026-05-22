from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base

class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, index=True)
    doctor_name = Column(String(100))
    specialization = Column(String(100))

    services = relationship("Service", back_populates="doctor")
    appointments = relationship("Appointment", back_populates="doctor")
