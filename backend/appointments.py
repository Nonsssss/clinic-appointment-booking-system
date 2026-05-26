from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from typing import Optional, List
from database.db import get_db
from models.appointment import Appointment as AppointmentModel
from models.service import Service as ServiceModel
from schemas.appointment import AppointmentCreate

router = APIRouter(prefix="/appointments", tags=["appointments"])


SERVICE_NAME_ALIASES = {
    "Medical Clearance for University Week": "Medical Clearance for U-Week"
}



def parse_appointment_start(appointment_date: str, appointment_time: str):
    raw_datetime = f"{appointment_date} {appointment_time.strip()}"
    accepted_formats = [
        "%Y-%m-%d %H:%M",
        "%Y-%m-%d %I:%M %p"
    ]

    for date_format in accepted_formats:
        try:
            return datetime.strptime(raw_datetime, date_format)
        except ValueError:
            continue

    raise HTTPException(
        status_code=400,
        detail="Invalid date or time format. Use YYYY-MM-DD with HH:MM or h:mm AM/PM"
    )


@router.get("") 
def list_appointments(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    
    
    if user_id:
       
        appointments = db.query(AppointmentModel).filter(AppointmentModel.user_id == user_id).all()
    else:
        appointments = db.query(AppointmentModel).all()
        
    results = []
    for app in appointments:
        service_name = app.service.service_name if app.service else "Unknown Service"
        
        results.append({
            "id": app.appointment_id,
            "patient_name": app.patient_name,
            "date": str(app.appointment_date),  
            "time": app.start_time.strftime("%I:%M %p"),  
            "service": service_name,
            "status": app.status
        })
        
    return results



@router.get("/availability/{service_id}/{date}")
def get_availability(service_id: int, date: str, db: Session = Depends(get_db)):

    try:
        target_date = datetime.strptime(date, "%Y-%m-%d").date()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format")

    service = db.query(ServiceModel).filter(
        ServiceModel.service_id == service_id
    ).first()

    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    booked = db.query(AppointmentModel).filter(
        AppointmentModel.appointment_date == target_date
    ).all()

    booked_slots = []

    for appt in booked:
        start = datetime.combine(appt.appointment_date, appt.start_time)
        end = datetime.combine(appt.appointment_date, appt.end_time)

        booked_slots.append({
            "start": start.isoformat(),
            "end": end.isoformat()
        })

    return {"booked": booked_slots}


@router.post("")
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    service = db.query(ServiceModel).filter(ServiceModel.service_id == payload.service_id).first()
    if service is None:
        raise HTTPException(status_code=400, detail="Invalid service")

    start_datetime = parse_appointment_start(payload.appointment_date, payload.appointment_time)
    end_datetime = start_datetime + timedelta(minutes=service.duration)
    
    if start_datetime < datetime.now():
        raise HTTPException(status_code=400, detail="Cannot book an appointment in the past")

    # CRITICAL CHANGE: Check overlaps across ALL bookings for that day, regardless of provider or service
    existing_appointments = db.query(AppointmentModel).filter(
        AppointmentModel.appointment_date == start_datetime.date()
    ).all()

    for existing in existing_appointments:
        existing_start = datetime.combine(existing.appointment_date, existing.start_time)
        existing_end = datetime.combine(existing.appointment_date, existing.end_time)

        # Global overlap conflict check
        if start_datetime < existing_end and end_datetime > existing_start:
            raise HTTPException(
                status_code=400,
                detail=f"Clinic is occupied. Next available slot: {existing_end.strftime('%I:%M %p')}"
            )

    # Create the globally validated appointment
    try:
        # 1. Create your database model object properly
        new_appointment = AppointmentModel(
            user_id=payload.user_id,
            patient_name=payload.fullname,
            service_id=payload.service_id,            
            appointment_date=start_datetime.date(),  
            start_time=start_datetime.time(),      
            end_time=end_datetime.time(),             
            status="pending",         
            slots_used=1
            
        )
        
        # 2. Add and commit to database
        db.add(new_appointment)
        db.commit()
        db.refresh(new_appointment)
        
        return {"status": "success", "message": "Appointment created"}

    except Exception as e:
        db.rollback() # 👈 CRITICAL: This undoes the save if Python crashes later!
        print(f"Backend error encountered: {str(e)}") # Prints the real error to terminal
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error or validation mismatch: {str(e)}"
        )

@router.get("/appointments/history/{user_id}", response_model=List[AppointmentCreate])
def get_appointment_history(user_id: int, db: Session = Depends(get_db)):
    # Query all appointments for this specific user, ordered by date (newest first)
    appointments = db.query(AppointmentModel).filter(
        AppointmentModel.user_id == user_id
    ).order_by(AppointmentModel.appointment_date.desc()).all()
    
    return appointments