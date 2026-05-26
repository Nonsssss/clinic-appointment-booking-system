from pydantic import BaseModel, Field

class AppointmentCreate(BaseModel):
    user_id: int
    fullname: str = Field(..., description="The patient's legal full name")
    service: str
    service_id: int
    appointment_date: str = Field(..., description="Format: YYYY-MM-DD")
    appointment_time: str = Field(..., description="Format: HH:MM or 12-hour AM/PM string")