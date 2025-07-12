def patient_schema(patient) -> dict:
    return {
        "id": str(patient["_id"]),
        "name": patient.get("name", ""),
        "last_name": patient.get("last_name", ""),
        "birth_date": patient.get("birth_date", ""),
        "age": patient.get("age", 0),
        "document": patient.get("document", 0),
        "weight_by_month": patient.get("weight_by_month", []),
        "cholesterol": patient.get("cholesterol", 0),
        "glucose": patient.get("glucose", 0),
        "conditions": patient.get("conditions", []),
        "medications": patient.get("medications", []),
        "activity_level": patient.get("activity_level", ""),
        "caretakers_ids": [str(cid) for cid in patient.get("caretakers_ids", [])],
        "medical_history": patient.get("medical_history", []),
        "meals": patient.get("meals", []),
        "medication_logs": patient.get("medication_logs", []),
        "hygiene_logs": patient.get("hygiene_logs", []),
        "vital_signs": patient.get("vital_signs", []),
        "symptoms": patient.get("symptoms", [])
    }

