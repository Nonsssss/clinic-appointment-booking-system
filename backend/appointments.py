from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from datetime import datetime, timedelta

router = APIRouter()

appointments = []

# Service durations in minutes
SERVICE_DURATIONS = {
    "Medical Clearance": 5,
    "Medical Clearance for Freshmen": 15,
    "Assessment for Internship": 15,
    "Dental Consultation": 20
}


class Appointment(BaseModel):
    fullname: str
    service: str
    appointment_date: str
    appointment_time: str


@router.post("/appointments")
def create_appointment(appointment: Appointment):

    if appointment.service not in SERVICE_DURATIONS:
        raise HTTPException(
            status_code=400,
            detail="Invalid service"
        )

    duration = SERVICE_DURATIONS[appointment.service]

    # Convert requested appointment to datetime
    start_datetime = datetime.strptime(
        f"{appointment.appointment_date} {appointment.appointment_time}",
        "%Y-%m-%d %H:%M"
    )

    end_datetime = start_datetime + timedelta(minutes=duration)

    # Check overlapping appointments
    for existing in appointments:

        existing_duration = SERVICE_DURATIONS[existing["service"]]

        existing_start = datetime.strptime(
            f"{existing['appointment_date']} {existing['appointment_time']}",
            "%Y-%m-%d %H:%M"
        )

        existing_end = existing_start + timedelta(
            minutes=existing_duration
        )

        # Overlap check
        if (
            start_datetime < existing_end
            and end_datetime > existing_start
        ):
            raise HTTPException(
                status_code=400,
                detail=(
                    f"Time conflict. "
                    f"Next available slot after "
                    f"{existing_end.strftime('%H:%M')}"
                )
            )

    new_appointment = {
        "fullname": appointment.fullname,
        "service": appointment.service,
        "appointment_date": appointment.appointment_date,
        "appointment_time": appointment.appointment_time,
        "end_time": end_datetime.strftime("%H:%M")
    }

    appointments.append(new_appointment)

    return {
        "message": "Appointment booked successfully",
        "appointment": new_appointment
    }


@router.get("/appointments")
def get_appointments():
    return appointments