from pydantic import BaseModel
# En este archivo se hace la clase base del patient y los atributos que contiene
from app.db.models.activity import MedicalHistoryEntry, Meal, MedicationLog, HygieneLog, VitalSigns, Symptom
from typing import List
from datetime import date
from typing import Optional

class Patient(BaseModel):
    id: Optional[str] = None
    name: str                      
    last_name: str                 
    birth_date: date
    age: int
    document: int
    # weight_by_month: List[WeightEntry] = []   # ← valor por defecto CUIDADO, POSIBLE ERROR
    cholesterol: Optional[int] = None         # opcional, si no lo quieres al inicio
    glucose: Optional[int] = None
    conditions: List[str] = []
    medications: List[str] = []
    activity_level: Optional[str] = None
    caretakers_ids: List[str] = []            # lista vacía por defecto
    medical_history: List[MedicalHistoryEntry] = []
    meals: List[Meal] = []
    medication_logs: List[MedicationLog] = []
    hygiene_logs: List[HygieneLog] = []
    vital_signs: List[VitalSigns] = []
    symptoms: List[Symptom] = []

