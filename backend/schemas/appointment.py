from pydantic import BaseModel

class AppointmentCreate(BaseModel):
    patient_name: str
    service_id: int
    appointment_date: str
    appointment_date: str
    appointment_time: str