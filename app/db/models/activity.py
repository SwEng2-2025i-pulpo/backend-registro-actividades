from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict

class MedicationLog(BaseModel):
    id: Optional[str] = None  # Para permitir la devolución con ObjectId convertido a string
    datetime: datetime
    medication_name: str
    dose: str
    route: str
    status: str
    observations: Optional[str] = ""


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


class VitalSigns(BaseModel):
    id: Optional[str] = None # puede ser opcional porque mongo asigna ids automaticos
    datetime: datetime
    blood_pressure: Dict[str, int]  # Ej: {"systolic": 130, "diastolic": 85}
    heart_rate: int
    observations: Optional[str] = ""


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


class WeightEntry(BaseModel):
    id: Optional[str] = None  # <-- nuevo campo agregado por Daniel opcional porque mongo lo pone
    month: str # formato YYYY-MM
    value: int # en kg
