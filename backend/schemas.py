from pydantic import BaseModel

class DoctorCreate(BaseModel):
    name: str
    specialty: str

class AppointmentCreate(BaseModel):
    patient_name: str
    doctor_id: int
