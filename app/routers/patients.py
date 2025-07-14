from fastapi import APIRouter, HTTPException, Body
from app.db.client import db_client
from bson import ObjectId
from datetime import datetime
from bson import ObjectId, errors as bson_errors
from app.db.schemas.activity import * 
from app.db.schemas.patient import *
from app.db.models.activity import MedicationLog, Meal, HygieneLog, VitalSigns, Symptom, MedicalHistoryEntry
from app.db.models.patient import Patient
from datetime import datetime, date

router = APIRouter(prefix="/patients", tags=["patients"])

#POST PACIENTE FUNCIONANDO
@router.post("/", response_model = Patient, summary="Crear un nuevo paciente", response_description="Paciente creado")

async def create_patient(patient_data: Patient):

    duplicated = search_duplicated(patient_data.document)
    if isinstance(duplicated, Patient):
        raise HTTPException(status_code=409, detail="El documento ya existe")

    patient_dict = dict(patient_data)
    del patient_dict["id"]

    # Convertir birth_date de date a datetime
    if isinstance(patient_dict["birth_date"], date):
        patient_dict["birth_date"] = datetime.combine(patient_dict["birth_date"], datetime.min.time())

     # Convertimos caretakers_ids de str a ObjectId si existe
    if "caretakers_ids" in patient_dict:
        patient_dict["caretakers_ids"] = [ObjectId(cid) for cid in patient_dict["caretakers_ids"]]

    ide = db_client.conectacare.patient.insert_one(patient_dict).inserted_id
    new_patient = patient_schema(db_client.conectacare.patient.find_one({"_id": ide}))
    return Patient(**new_patient)


def search_duplicated(document: int):
    patient_found = db_client.conectacare.patient.find_one({"document": document})
    if patient_found:
        return Patient(**patient_schema(patient_found))
    return None
    

# #GET POR ID FUNCIONANDO
@router.get("/patients/{patient_id}", summary="Obtener paciente por ID")
async def get_patient_by_id(patient_id: str):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="ID de paciente inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    try:
        return patient_schema(patient)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al procesar el paciente: {str(e)}")

# #GET PATIENTS FUNCIONANDO función en el otro backend 3002
# @router.get("/", summary="Obtener lista de pacientes", response_description="Lista de pacientes")
# async def get_patients():

#     patients = patient_schema_starting_list(db_client.conectacare.patient.find())
#     return patients

#POST FUNCIONANDO
@router.post("/{patient_id}/medication_logs", response_model=MedicationLog, summary="Registrar medicación para un paciente", response_description="Medicación registrada")
async def add_medication_log(patient_id: str, medication_log: MedicationLog):
    """
    Registra un nuevo evento de administración de medicación para el paciente especificado.
    """

    # Validar formato de ObjectId
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    # Verificar si el paciente existe
    patient = db_client.conectacare.patient.find_one({"_id": object_id}) #verificamos que el patient existe
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Convertir a dict y agregar el campo `id` con un nuevo ObjectId
    medication_log_data = medication_log.dict()
    medication_log_data["id"] = ObjectId()

    # Agregar el nuevo registro al arreglo de medication_logs
    result = db_client.conectacare.patient.update_one(
        {"_id": object_id},
        {"$push": {"medication_logs": medication_log_data}}
    )

    if result.modified_count == 1:
        return MedicationLog(**medication_log_schema(medication_log_data))

    raise HTTPException(status_code=400, detail="No se pudo agregar el registro")

#GET FUNCIONANDO
@router.get("/{patient_id}/medication_logs", summary="Obtener registros de medicación de un paciente", response_description="Lista de registros de medicación")
async def get_medication_logs(patient_id: str):

    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})

    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    medication_logs = patient.get("medication_logs", [])

    return medication_logs_schema(medication_logs)

#PUT FUNCIONANDO
@router.put("/{patient_id}/medication_logs/{log_id}", response_model=MedicationLog, summary="Actualizar un registro de medicación de un paciente", response_description="Registro de medicación actualizado")
async def update_medication_log(patient_id: str, log_id: str, updated_log: MedicationLog):

    try:
        object_id = ObjectId(patient_id)
        log_id_object = ObjectId(log_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id o log_id inválido")

    updated_log_dict = updated_log.dict()

    updated_log_dict["id"] = log_id_object

    result = db_client.conectacare.patient.update_one(
        {"_id": object_id, "medication_logs.id": log_id_object},
        {"$set": {"medication_logs.$": updated_log_dict}}
    )

    if result.modified_count == 1:
        return MedicationLog(**medication_log_schema(updated_log_dict))

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")

#POST FUNCIONANDO
@router.post("/{patient_id}/meals", response_model= Meal, summary="Registrar comida para un paciente", response_description="Comida registrada")
async def add_meal(patient_id: str, meal: Meal):
    try:
        id_del_paciente = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")
    
    patient = db_client.conectacare.patient.find_one({"_id": id_del_paciente}) #verificamos que el patient existe
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    comida_a_agregar = meal.dict()
    comida_a_agregar["id"] = ObjectId() #asignamos el _id porque como hacemos un update y no un insert, mongo no lo asigna automaticamente.


    result = db_client.conectacare.patient.update_one(
        {"_id": id_del_paciente},
        {"$push": {"meals": comida_a_agregar}}
    )    
    
    if result.modified_count == 1:
        return Meal(**meal_schema(comida_a_agregar))
    
    raise HTTPException(status_code=400, detail="No se pudo agregar el registro")

#GET FUNCIONANDO
@router.get("/{patient_id}/meals", summary="Obtener registros de comidas de un paciente", response_description="Lista de registros de comidas")
async def get_meals(patient_id: str):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    meals = patient.get("meals", [])

    return meals_schema(meals)

#PUT FUNCIONANDO
@router.put("/{patient_id}/meals/{meal_id}", response_model=Meal, summary="Actualizar un registro de comida de un paciente", response_description="Registro de comida actualizado")
async def update_meal(patient_id: str, meal_id: str, updated_meal: Meal):

    try:
        object_id = ObjectId(patient_id)
        meal_id_object = ObjectId(meal_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id o meal_id inválido")
    
    
    updated_meal_dict = updated_meal.dict()
    updated_meal_dict["id"]= meal_id_object

    result = db_client.conectacare.patient.update_one(
        {"_id": object_id, "meals.id": meal_id_object},
        {"$set": {"meals.$": updated_meal_dict}}
    )

    if result.modified_count == 1:
        return Meal(**meal_schema(updated_meal_dict))

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")

#POST FUNCIONANDO
@router.post("/{patient_id}/hygiene_logs",response_model=HygieneLog, summary="Registrar evento de higiene para un paciente", response_description="Evento de higiene registrado")
async def add_hygiene_log(patient_id: str, hygiene_log: HygieneLog):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    hygiene_log_dict = hygiene_log.dict()
    hygiene_log_dict["id"] = ObjectId()

    result = db_client.conectacare.patient.update_one(
        {"_id": object_id},
        {"$push": {"hygiene_logs": hygiene_log_dict}}
    )

    if result.modified_count == 1:
        return HygieneLog(**hygiene_log_schema(hygiene_log_dict))

    raise HTTPException(status_code=400, detail="No se pudo agregar el registro")

#GET FUNCIONANDO
@router.get("/{patient_id}/hygiene_logs", summary="Obtener registros de higiene de un paciente", response_description="Lista de registros de higiene")
async def get_hygiene_logs(patient_id: str):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    hygiene_logs = patient.get("hygiene_logs", [])

    return hygiene_logs_schema(hygiene_logs)

# PUT FUNCIONANDO
@router.put("/{patient_id}/hygiene_logs/{hygiene_id}", response_model=HygieneLog, summary="Actualizar un registro de higiene de un paciente", response_description="Registro de higiene actualizado")
async def update_hygiene_log(patient_id: str, hygiene_id: str, updated_log: HygieneLog):

    try:
        object_id = ObjectId(patient_id)
        hygiene_id_object = ObjectId(hygiene_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id ó hygiene_id inválido")
    

    updated_log_dict = updated_log.dict()
    updated_log_dict["id"] = hygiene_id_object

    result = db_client.conectacare.patient.update_one(
        {"_id": object_id, "hygiene_logs.id": hygiene_id_object},
        {"$set": {"hygiene_logs.$": updated_log_dict}}
    )

    if result.modified_count == 1:
        return HygieneLog(**hygiene_log_schema(updated_log_dict))

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")

#POST FUNCIONANDO
@router.post("/{patient_id}/vital_signs", response_model=VitalSigns, summary="Registrar signos vitales para un paciente", response_description="Signos vitales registrados")
async def add_vital_signs(patient_id: str, vital_signs: VitalSigns):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    vital_signs_dict = vital_signs.dict()
    vital_signs_dict["id"] = ObjectId()

    # for item in vital_signs_dict["weight_by_month"]:
    #     item["id"] = ObjectId()

    result = db_client.conectacare.patient.update_one(
        {"_id": object_id},
        {"$push": {"vital_signs": vital_signs_dict}}
    )

    if result.modified_count == 1:
        return VitalSigns(**vital_sign_schema(vital_signs_dict))

    raise HTTPException(status_code=400, detail="No se pudo agregar el registro")

#GET FUNCIONANDO
@router.get("/{patient_id}/vital_signs", summary="Obtener registros de signos vitales de un paciente", response_description="Lista de registros de signos vitales")
async def get_vital_signs(patient_id: str):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    vital_signs = patient.get("vital_signs", [])

    return vital_signs_schema(vital_signs)

#EN PROGRESO
@router.put("/{patient_id}/vital_signs/{vital_id}", response_model=VitalSigns, summary="Actualizar un registro de signos vitales de un paciente", response_description="Registro de signos vitales actualizado")
def update_vital_signs(patient_id: str, vital_id: str, updated_signs: VitalSigns):

    try:
        object_id = ObjectId(patient_id)
        vital_id_object = ObjectId(vital_id)

    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    updated_signs_dict = updated_signs.dict()
    updated_signs_dict["id"] = vital_id_object

    result = db_client.conectacare.patient.update_one(
        {"_id": object_id, "vital_signs.id": vital_id_object},
        {"$set": {"vital_signs.$": updated_signs_dict}}
    )

    if result.modified_count == 1:
        return VitalSigns(**vital_sign_schema(updated_signs_dict))

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")


#POST FUNCIONANDO
@router.post("/{patient_id}/symptoms", response_model=Symptom, summary="Registrar síntoma para un paciente", response_description="Síntoma registrado")
async def add_symptom(patient_id: str, symptom: Symptom):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    symptom_dict = symptom.dict()
    symptom_dict["id"] = ObjectId()

    result = db_client.conectacare.patient.update_one(
        {"_id": object_id},
        {"$push": {"symptoms": symptom_dict}}
    )

    if result.modified_count == 1:
        return Symptom(**symptom_schema(symptom_dict))

    raise HTTPException(status_code=400, detail="No se pudo agregar el registro")

#GET FUNCIONANDO
@router.get("/{patient_id}/symptoms", summary="Obtener registros de síntomas de un paciente", response_description="Lista de registros de síntomas")
async def get_symptoms(patient_id: str):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    symptoms = patient.get("symptoms", [])

    return symptoms_schema(symptoms)

#PUT FUNCIONANDO
@router.put("/{patient_id}/symptoms/{symptom_id}", response_model= Symptom, summary="Actualizar un registro de síntomas de un paciente", response_description="Registro de síntoma actualizado")
async def update_symptom(patient_id: str, symptom_id: str, updated_symptom: Symptom):

    try:
        object_id = ObjectId(patient_id)
        symptom_id_log = ObjectId(symptom_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    updated_symptom_dict = updated_symptom.dict()
    updated_symptom_dict["id"] = symptom_id_log

    result = db_client.conectacare.patient.update_one(
        {"_id": object_id, "symptoms.id": symptom_id_log},
        {"$set": {"symptoms.$": updated_symptom_dict}}
    )

    if result.modified_count == 1:
        return Symptom(**symptom_schema(updated_symptom_dict))

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")

#POST FUNCIONANDO
@router.post("/{patient_id}/medical_history", response_model=MedicalHistoryEntry, summary="Registrar entrada en historial médico de un paciente", response_description="Entrada en historial médico registrada")
async def add_medical_history_entry(patient_id: str, entry: MedicalHistoryEntry):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    entry_dict = entry.dict()
    entry_dict["id"] = ObjectId()
    
    result = db_client.conectacare.patient.update_one(
        {"_id": object_id},
        {"$push": {"medical_history": entry_dict}}
    )

    if result.modified_count == 1:
        return MedicalHistoryEntry(**medical_history_entry_schema(entry_dict))

    raise HTTPException(status_code=400, detail="No se pudo agregar el registro")

#GET FUNCIONANDO
@router.get("/{patient_id}/medical_history", summary="Obtener historial médico de un paciente", response_description="Historial médico")
async def get_medical_history(patient_id: str):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = db_client.conectacare.patient.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    medical_history = patient.get("medical_history", [])

    return medical_history_schema(medical_history)

#PUT FUNCIONANDO
@router.put("/{patient_id}/medical_history/{medical_history_id}", response_model= MedicalHistoryEntry, summary="Actualizar un registro del historial médico de un paciente", response_description="Registro del historial médico actualizado")
async def update_medical_history_entry(patient_id: str, medical_history_id: str, updated_entry: MedicalHistoryEntry):

    try:
        object_id = ObjectId(patient_id)
        medical_history_id_object = ObjectId(medical_history_id)

    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    updated_entry_dict = updated_entry.dict()
    updated_entry_dict["id"] = medical_history_id_object

    result = db_client.conectacare.patient.update_one(
        {"_id": object_id, "medical_history.id": medical_history_id_object},
        {"$set": {"medical_history.$": updated_entry_dict}}
    )

    if result.modified_count == 1:
        return MedicalHistoryEntry(**medical_history_entry_schema(updated_entry_dict))

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")