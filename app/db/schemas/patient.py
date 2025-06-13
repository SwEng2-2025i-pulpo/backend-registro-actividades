def patient_schema(patient) -> dict:
    return {
        "id": str(patient["_id"]),
        "full_name": patient.get("full_name", ""),
        "birth_date": patient.get("birth_date", ""),
        "age": patient.get("age", ""),
        "weight_by_month": patient.get("weight_by_month", []),
        "cholesterol": patient.get("cholesterol", ""),
        "glucose": patient.get("glucose", ""),
        "conditions": patient.get("conditions", []),
        "medications": patient.get("medications", []),
        "activity_level": patient.get("activity_level", ""),
        "caretaker_id": str(patient.get("caretaker_id", "")),
        "medical_history": patient.get("medical_history", []),
        "meals": patient.get("meals", []),
        "medication_logs": patient.get("medication_logs", []),
        "hygiene_logs": patient.get("hygiene_logs", []),
        "vital_signs": patient.get("vital_signs", []),
        "symptoms": patient.get("symptoms", [])
    }
