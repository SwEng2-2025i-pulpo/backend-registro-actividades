from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class MedicationLog(BaseModel):
    datetime: datetime
    medication_name: str
    dose: str
    route: str
    status: str
    observations: Optional[str] = ""


class Meal(BaseModel):
    datetime: datetime
    meal_type: str
    description: str
    hydration: str
    observations: Optional[str] = ""


class HygieneLog(BaseModel):
    datetime: datetime
    type: str
    condition: str
    status: str
    assistance_level: str
    observations: Optional[str] = ""


class VitalSigns(BaseModel):
    datetime: datetime
    blood_pressure: Dict[str, int]  # Ej: {"systolic": 130, "diastolic": 85}
    heart_rate: int
    observations: Optional[str] = ""


class Symptom(BaseModel):
    datetime: datetime
    description: str
    observations: Optional[str] = ""


class MedicalHistoryEntry(BaseModel):
    date: datetime
    description: str
    notes: Optional[str] = ""


class WeightEntry(BaseModel):
    month: str # formato YYYY-MM
    value: int # en kg
