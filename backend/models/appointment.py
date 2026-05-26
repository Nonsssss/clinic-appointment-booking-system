from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class Appointment(Base):
    __tablename__ = "appointments"

    appointment_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    patient_name = Column(String(100))
    service_id = Column(Integer, ForeignKey("services.service_id"))
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"))

    appointment_date = Column(Date)
    start_time = Column(Time)
    end_time = Column(Time)

    status = Column(String(50))
    slots_used = Column(Integer)

    service = relationship("Service", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")
