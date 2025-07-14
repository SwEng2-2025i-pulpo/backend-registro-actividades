
from bson import ObjectId
from datetime import datetime

def to_str_id(obj):
    if isinstance(obj, dict) and "id" in obj and isinstance(obj["id"], ObjectId): # es para devolver los ids de los arrays del paciente.
        obj["id"] = str(obj["id"])
    return obj

def patient_schema(patient) -> dict:
    return {
        "id": str(patient["_id"]),
        "name": patient.get("name", ""),
        "last_name": patient.get("last_name", ""),
        "birth_date": patient["birth_date"].date().isoformat() if "birth_date" in patient else "",
        "age": patient.get("age", 0),
        "document": patient.get("document", 0),
        "cholesterol": patient.get("cholesterol", 0),
        "glucose": patient.get("glucose", 0),
        "conditions": patient.get("conditions", []),
        "medications": patient.get("medications", []),
        "activity_level": patient.get("activity_level", ""),
        "caretakers_ids": [str(cid) for cid in patient.get("caretakers_ids", [])],
        "medical_history": [to_str_id(h) for h in patient.get("medical_history", [])],
        "meals": [to_str_id(m) for m in patient.get("meals", [])],
        "medication_logs": [to_str_id(m) for m in patient.get("medication_logs", [])],
        "hygiene_logs": [to_str_id(h) for h in patient.get("hygiene_logs", [])],
        "vital_signs": [to_str_id(v) for v in patient.get("vital_signs", [])],
        "symptoms": [to_str_id(s) for s in patient.get("symptoms", [])]
    }

