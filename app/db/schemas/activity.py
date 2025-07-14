def medication_log_schema(log) -> dict:
    return {
        "id": str(log["id"]),  # <-- este es clave
        "datetime": log["datetime"],
        "medication_name": log["medication_name"],
        "dose": log["dose"],
        "route": log["route"],
        "status": log["status"],
        "observations": log.get("observations", "")
    }


def medication_logs_schema(logs) -> list:
    return [medication_log_schema(log) for log in logs]


def meal_schema(meal) -> dict:
    return {
        "id": str(meal["id"]),
        "datetime": meal["datetime"],
        "meal_type": meal["meal_type"],
        "description": meal["description"],
        "hydration": meal["hydration"],
        "observations": meal.get("observations", "")
    }

def meals_schema(meals) -> list:
    return [meal_schema(meal) for meal in meals]


def hygiene_log_schema(log) -> dict:
    return {
        "id": str(log["id"]),
        "datetime": log["datetime"],
        "type": log["type"],
        "condition": log["condition"],
        "status": log["status"],
        "assistance_level": log["assistance_level"],
        "observations": log.get("observations", "")
    }

def hygiene_logs_schema(logs) -> list:
    return [hygiene_log_schema(log) for log in logs]


# Helper function for blood_pressure sub-document
def blood_pressure_schema(bp_record) -> dict:
    return {
        "systolic": bp_record["systolic"],
        "diastolic": bp_record["diastolic"]
    }

# Main vital_sign_schema
def vital_sign_schema(sign) -> dict:
    return {
        "id": str(sign["id"]), # Convert ObjectId to string for client-side use
        "datetime": sign["datetime"],
        "daily_weight": sign["daily_weight"],
        "blood_pressure": blood_pressure_schema(sign["blood_pressure"]), # Process blood pressure object
        "heart_rate": sign["heart_rate"],
        "observations": sign["observations"] # Now treated as required, will raise KeyError if missing
    }

def vital_signs_schema(signs) -> list:
    return [vital_sign_schema(sign) for sign in signs]


def symptom_schema(symptom) -> dict:
    return {
        "id": str(symptom["id"]),
        "datetime": symptom["datetime"],
        "description": symptom["description"],
        "observations": symptom.get("observations", "")
    }

def symptoms_schema(symptoms) -> list:
    return [symptom_schema(symptom) for symptom in symptoms]


def medical_history_entry_schema(entry) -> dict:
    return {
        "id": str(entry.get("id", "")), # agregado por Danny
        "date": entry["date"],
        "description": entry["description"],
        "notes": entry.get("notes", "")
    }

def medical_history_schema(entries) -> list:
    return [medical_history_entry_schema(entry) for entry in entries]
