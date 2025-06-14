from pydantic import BaseModel
# En este archivo se hace la clase base del patient y los atributos que contiene
from app.db.models.activity import WeightEntry, MedicalHistoryEntry, Meal, MedicationLog, HygieneLog, VitalSigns, Symptom
from typing import List
from datetime import date


class Patient(BaseModel):

    id: str | None = None # volvemos el id opcional porque mongo lo pone automaticamente lo ponemos str porque mongo trabaja así
    full_name: str
    birth_date: date
    age: int
    weight_by_month: List[WeightEntry]
    cholesterol: int
    glucose: int
    conditions: List[str]
    medications: List[str]
    activity_level: str  # Bajo, Moderado, Alto
    caretaker_id: str  # se maneja como string (puedes convertir a ObjectId si usas pymongo)
    medical_history: List[MedicalHistoryEntry]
    meals: List[Meal]
    medication_logs: List[MedicationLog]
    hygiene_logs: List[HygieneLog]
    vital_signs: List[VitalSigns]
    symptoms: List[Symptom]