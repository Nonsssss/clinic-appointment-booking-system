from sqlalchemy import Column, Integer, String, ForeignKey
from database.db import Base

class Service(Base):
    __tablename__ = "services"

    service_id = Column(Integer, primary_key=True, index=True)
    service_name = Column(String(100))
    duration = Column(Integer)
    slots_required = Column(Integer)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"))