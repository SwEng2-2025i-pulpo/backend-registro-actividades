from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, List


class MedicationLog(BaseModel):
    
    datetime: datetime
    medication_name: str
    dose: str
    route: str
    status: str
    observations: Optional[str] = ""
    id: Optional[str] = None  # Para permitir la devolución con ObjectId convertido a string


class Meal(BaseModel):
    id: Optional[str] = None # puede ser opcional porque mongo asigna ids automaticos
    datetime: datetime
    meal_type: str
    description: str
    hydration: str
    observations: Optional[str] = ""


class HygieneLog(BaseModel):
    id: Optional[str] = None # puede ser opcional porque mongo asigna ids automaticos
    datetime: datetime
    type: str
    condition: str
    status: str
    assistance_level: str
    observations: Optional[str] = ""
    

# Sub-model for blood pressure
class BloodPressure(BaseModel):
    systolic: int
    diastolic: int

# Main VitalSigns model
class VitalSigns(BaseModel):
    id: Optional[str] = None
    datetime: datetime
    daily_weight: int
    blood_pressure: BloodPressure
    heart_rate: int
    observations: str



class Symptom(BaseModel):
    id: Optional[str] = None # puede ser opcional porque mongo asigna ids automaticos
    datetime: datetime
    description: str
    observations: Optional[str] = ""


class MedicalHistoryEntry(BaseModel):
    id: Optional[str] = None  # <-- cambio hecho por Danny
    date: datetime
    description: str
    notes: Optional[str] = ""

