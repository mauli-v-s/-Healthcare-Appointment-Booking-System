from fastapi import FastAPI, HTTPException, Depends
from database import engine, Base, SessionLocal
from models import Doctor, Appointment
from schemas import DoctorCreate, AppointmentCreate
from sqlalchemy.orm import Session
from database import engine, Base
from schemas import DoctorCreate, AppointmentCreate



Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/doctors/")
def add_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    new_doctor = Doctor(**doctor.dict())
    db.add(new_doctor)
    db.commit()
    return {"message": "Doctor added successfully"}

@app.get("/doctors/")
def get_doctors(db: Session = Depends(get_db)):
    return db.query(Doctor).all()

@app.get("/doctors/{doctor_id}")
def get_doctor_by_id(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.post("/doctors/{doctor_id}/appointments/")
def book_appointment(doctor_id: int, appointment: AppointmentCreate, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    new_appointment = Appointment(**appointment.dict(), doctor_id=doctor_id)
    db.add(new_appointment)
    db.commit()
    return {"message": "Appointment booked successfully"}

@app.delete("/appointments/{appointment_id}")
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    db.delete(appointment)
    db.commit()
    return {"message": "Appointment canceled successfully"}