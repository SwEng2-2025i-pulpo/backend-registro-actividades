from fastapi import APIRouter, HTTPException, Body
from app.db.client import db_client
from bson import ObjectId
from datetime import datetime
from bson import ObjectId, errors as bson_errors
from app.db.schemas.activity import medication_log_schema, medication_logs_schema,meal_schema, meals_schema, hygiene_logs_schema, vital_signs_schema, symptoms_schema, medical_history_schema
from app.db.schemas.patient import patient_schema
from app.db.models.activity import MedicationLog, Meal, HygieneLog, VitalSigns, Symptom, MedicalHistoryEntry
from app.db.models.patient import Patient
from datetime import datetime, date

router = APIRouter(prefix="/patients", tags=["patients"])

# Definir la colección de pacientes
patients_collection = db_client["conectacare"]["patient"]

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
    
#GET POR ID FUNCIONANDO
@router.get("/{patient_id}", summary="Obtener paciente por id", response_description="Paciente por id")
async def get_patientid(patient_id: str): #cambio función ASYNC Daniel 11 JULIO
    return search_patientsid("_id", ObjectId(patient_id))

    #patientById = patients_collection.find_one({"_id":patientId})

def search_patientsid(field: str, key): # función para obtener un patient
    try:
        searcher = patient_schema(db_client.conectacare.patient.find_one({field: key}))
        return Patient(**searcher)
    except:
        return {"error": "no se ha encontrado el usuario getbyid"}


@router.get("/", summary="Obtener lista de pacientes", response_description="Lista de pacientes")
def get_patients():
    """
    Obtiene la lista completa de pacientes registrados en la base de datos.

    Retorna:
    - Lista de pacientes, cada uno con su ID, nombre y edad.
    """
    patients = list(patients_collection.find())
    return [
        {
            "id": str(patient["_id"]),
            "name": patient.get("full_name", "Sin nombre"),
            "age": patient.get("age", "Sin edad")
        }
        for patient in patients
    ]

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
    patient = patients_collection.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # Convertir a dict y agregar el campo `id` con un nuevo ObjectId
    medication_log_data = medication_log.dict()
    medication_log_data["id"] = ObjectId()

    # Agregar el nuevo registro al arreglo de medication_logs
    result = patients_collection.update_one(
        {"_id": object_id},
        {"$push": {"medication_logs": medication_log_data}}
    )

  
    if result.modified_count == 1:
        return MedicationLog(**medication_log_schema(medication_log_data))

    raise HTTPException(status_code=500, detail="No se pudo agregar el registro")


@router.get("/{patient_id}/medication_logs", summary="Obtener registros de medicación de un paciente", response_description="Lista de registros de medicación")
def get_medication_logs(patient_id: str):
    """
    Obtiene todos los registros de medicación del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.

    Retorna:
    - Lista de registros de medicación.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = patients_collection.find_one({"_id": object_id})

    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    medication_logs = patient.get("medication_logs", [])

    return medication_logs_schema(medication_logs)


@router.put("/{patient_id}/medication_logs", summary="Actualizar un registro de medicación de un paciente", response_description="Registro de medicación actualizado")
def update_medication_log(patient_id: str, updated_log: MedicationLog):
    """
    Actualiza un registro específico de medicación del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.
    - updated_log (en el body): Registro completo de medicación. Se usará el campo `datetime` como identificador.

    Retorna:
    - Mensaje de éxito si el registro fue actualizado.
    - Error 404 si no se encontró el registro a actualizar.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    updated_datetime = updated_log.datetime

    updated_log_dict = updated_log.dict()
    updated_log_dict["datetime"] = updated_datetime

    result = patients_collection.update_one(
        {"_id": object_id, "medication_logs.datetime": updated_datetime},
        {"$set": {"medication_logs.$": updated_log_dict}}
    )

    if result.modified_count == 1:
        return {"message": "Registro de medicación actualizado exitosamente"}

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")


# @router.post("/{patient_id}/meals", summary="Registrar comida para un paciente", response_description="Comida registrada")
# def add_meal(patient_id: str, meal: Meal):
#     try:
#         object_id = ObjectId(patient_id)
#     except bson_errors.InvalidId:
#         raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

#     patient = patients_collection.find_one({"_id": object_id})
#     if not patient:
#         raise HTTPException(status_code=404, detail="Paciente no encontrado")

#     meal_dict = meal.dict()

#     result = patients_collection.update_one(
#         {"_id": object_id},
#         {"$push": {"meals": meal_dict}}
#     )

#     if result.modified_count == 1:
#         return {"message": "Registro de comida agregado exitosamente"}

#     raise HTTPException(status_code=500, detail="No se pudo agregar el registro")

@router.post("/{patient_id}/meals", response_model= Meal, summary="Registrar comida para un paciente", response_description="Comida registrada")
async def add_meal(patient_id: str, meal: Meal):
    try:
        id_del_paciente = (ObjectId(patient_id))
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")
    
    patient = db_client.conectacare.patient.find_one({"_id": id_del_paciente}) #verificamos que el patient existe
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    comida_a_agregar = meal.dict()
    comida_a_agregar["_id"] = ObjectId() #asignamos el _id porque como hacemos un update y no un insert, mongo no lo asigna automaticamente.


    result = db_client.conectacare.patient.update_one(
        {"_id": id_del_paciente},
        {"$push": {"meals": comida_a_agregar}}
    )    
    
    if result.modified_count == 1:
        return meal_schema(comida_a_agregar)
    
    raise HTTPException(status_code=400, detail="No se pudo agregar el registro")
 #   ----------------------- Antigua función usando colecciones
    # try:
    #     object_id = ObjectId(patient_id)
    # except bson_errors.InvalidId:
    #     raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    # patient = patients_collection.find_one({"_id": object_id})
    # if not patient:
    #     raise HTTPException(status_code=404, detail="Paciente no encontrado")

    # meal_dict = meal.dict()
    # meal_dict["id"] = ObjectId()  # ✅ Este campo lo exige tu esquema de MongoDB



@router.get("/{patient_id}/meals", summary="Obtener registros de comidas de un paciente", response_description="Lista de registros de comidas")
def get_meals(patient_id: str):
    """
    Obtiene todos los registros de comidas del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.

    Retorna:
    - Lista de registros de comidas.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = patients_collection.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    meals = patient.get("meals", [])

    return meals_schema(meals)


@router.put("/{patient_id}/meals", summary="Actualizar un registro de comida de un paciente", response_description="Registro de comida actualizado")
def update_meal(patient_id: str, updated_meal: Meal):
    """
    Actualiza un registro específico de comida del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.
    - updated_meal (en el body): Registro completo de comida. Se usará el campo `datetime` como identificador.

    Retorna:
    - Mensaje de éxito si el registro fue actualizado.
    - Error 404 si no se encontró el registro a actualizar.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    updated_datetime = updated_meal.datetime

    updated_meal_dict = updated_meal.dict()
    updated_meal_dict["datetime"] = updated_datetime

    result = patients_collection.update_one(
        {"_id": object_id, "meals.datetime": updated_datetime},
        {"$set": {"meals.$": updated_meal_dict}}
    )

    if result.modified_count == 1:
        return {"message": "Registro de comida actualizado exitosamente"}

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")


@router.post("/{patient_id}/hygiene_logs", summary="Registrar evento de higiene para un paciente", response_description="Evento de higiene registrado")
def add_hygiene_log(patient_id: str, hygiene_log: HygieneLog):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = patients_collection.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    hygiene_log_dict = hygiene_log.dict()

    result = patients_collection.update_one(
        {"_id": object_id},
        {"$push": {"hygiene_logs": hygiene_log_dict}}
    )

    if result.modified_count == 1:
        return {"message": "Registro de evento de higiene agregado exitosamente"}

    raise HTTPException(status_code=500, detail="No se pudo agregar el registro")


@router.get("/{patient_id}/hygiene_logs", summary="Obtener registros de higiene de un paciente", response_description="Lista de registros de higiene")
def get_hygiene_logs(patient_id: str):
    """
    Obtiene todos los registros de eventos de higiene del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.

    Retorna:
    - Lista de registros de higiene.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = patients_collection.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    hygiene_logs = patient.get("hygiene_logs", [])

    return hygiene_logs_schema(hygiene_logs)


@router.put("/{patient_id}/hygiene_logs", summary="Actualizar un registro de higiene de un paciente", response_description="Registro de higiene actualizado")
def update_hygiene_log(patient_id: str, updated_log: HygieneLog):
    """
    Actualiza un registro específico de higiene del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.
    - updated_log (en el body): Registro completo de higiene. Se usará el campo `datetime` como identificador.

    Retorna:
    - Mensaje de éxito si el registro fue actualizado.
    - Error 404 si no se encontró el registro a actualizar.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    updated_datetime = updated_log.datetime

    updated_log_dict = updated_log.dict()
    updated_log_dict["datetime"] = updated_datetime

    result = patients_collection.update_one(
        {"_id": object_id, "hygiene_logs.datetime": updated_datetime},
        {"$set": {"hygiene_logs.$": updated_log_dict}}
    )

    if result.modified_count == 1:
        return {"message": "Registro de higiene actualizado exitosamente"}

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")


@router.post("/{patient_id}/vital_signs", summary="Registrar signos vitales para un paciente", response_description="Signos vitales registrados")
def add_vital_signs(patient_id: str, vital_signs: VitalSigns):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = patients_collection.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    vital_signs_dict = vital_signs.dict()

    result = patients_collection.update_one(
        {"_id": object_id},
        {"$push": {"vital_signs": vital_signs_dict}}
    )

    if result.modified_count == 1:
        return {"message": "Registro de signos vitales agregado exitosamente"}

    raise HTTPException(status_code=500, detail="No se pudo agregar el registro")


@router.get("/{patient_id}/vital_signs", summary="Obtener registros de signos vitales de un paciente", response_description="Lista de registros de signos vitales")
def get_vital_signs(patient_id: str):
    """
    Obtiene todos los registros de signos vitales del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.

    Retorna:
    - Lista de registros de signos vitales.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = patients_collection.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    vital_signs = patient.get("vital_signs", [])

    return vital_signs_schema(vital_signs)


@router.put("/{patient_id}/vital_signs", summary="Actualizar un registro de signos vitales de un paciente", response_description="Registro de signos vitales actualizado")
def update_vital_signs(patient_id: str, updated_signs: VitalSigns):
    """
    Actualiza un registro específico de signos vitales del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.
    - updated_signs (en el body): Registro completo de signos vitales. Se usará el campo `datetime` como identificador.

    Retorna:
    - Mensaje de éxito si el registro fue actualizado.
    - Error 404 si no se encontró el registro a actualizar.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    updated_datetime = updated_signs.datetime

    updated_signs_dict = updated_signs.dict()
    updated_signs_dict["datetime"] = updated_datetime

    result = patients_collection.update_one(
        {"_id": object_id, "vital_signs.datetime": updated_datetime},
        {"$set": {"vital_signs.$": updated_signs_dict}}
    )

    if result.modified_count == 1:
        return {"message": "Registro de signos vitales actualizado exitosamente"}

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")


@router.post("/{patient_id}/symptoms", summary="Registrar síntoma para un paciente", response_description="Síntoma registrado")
def add_symptom(patient_id: str, symptom: Symptom):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = patients_collection.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    symptom_dict = symptom.dict()

    result = patients_collection.update_one(
        {"_id": object_id},
        {"$push": {"symptoms": symptom_dict}}
    )

    if result.modified_count == 1:
        return {"message": "Registro de síntoma agregado exitosamente"}

    raise HTTPException(status_code=500, detail="No se pudo agregar el registro")


@router.get("/{patient_id}/symptoms", summary="Obtener registros de síntomas de un paciente", response_description="Lista de registros de síntomas")
def get_symptoms(patient_id: str):
    """
    Obtiene todos los registros de síntomas del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.

    Retorna:
    - Lista de registros de síntomas.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = patients_collection.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    symptoms = patient.get("symptoms", [])

    return symptoms_schema(symptoms)


@router.put("/{patient_id}/symptoms", summary="Actualizar un registro de síntomas de un paciente", response_description="Registro de síntoma actualizado")
def update_symptom(patient_id: str, updated_symptom: Symptom):
    """
    Actualiza un registro específico de síntomas del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.
    - updated_symptom (en el body): Registro completo de síntoma. Se usará el campo `datetime` como identificador.

    Retorna:
    - Mensaje de éxito si el registro fue actualizado.
    - Error 404 si no se encontró el registro a actualizar.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    updated_datetime = updated_symptom.datetime

    updated_symptom_dict = updated_symptom.dict()
    updated_symptom_dict["datetime"] = updated_datetime

    result = patients_collection.update_one(
        {"_id": object_id, "symptoms.datetime": updated_datetime},
        {"$set": {"symptoms.$": updated_symptom_dict}}
    )

    if result.modified_count == 1:
        return {"message": "Registro de síntoma actualizado exitosamente"}

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")


@router.post("/{patient_id}/medical_history", summary="Registrar entrada en historial médico de un paciente", response_description="Entrada en historial médico registrada")
def add_medical_history_entry(patient_id: str, entry: MedicalHistoryEntry):
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = patients_collection.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    entry_dict = entry.dict()

    result = patients_collection.update_one(
        {"_id": object_id},
        {"$push": {"medical_history": entry_dict}}
    )

    if result.modified_count == 1:
        return {"message": "Registro en historial médico agregado exitosamente"}

    raise HTTPException(status_code=500, detail="No se pudo agregar el registro")


# @router.get("/{patient_id}/medical_history", summary="Obtener historial médico de un paciente", response_description="Historial médico")
# def get_medical_history(patient_id: str):
#     """
#     Obtiene todas las entradas del historial médico del paciente especificado.
#     """
#     try:
#         object_id = ObjectId(patient_id)
#     except bson_errors.InvalidId:
#         raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

#     patient = search_patientsidnew("_id", object_id)
#     return patient.medical_history

# def search_patientsidnew(field: str, key):
#     raw_patient = db_client.conectacare.patient.find_one({field: key})
#     if not raw_patient:
#         raise HTTPException(status_code=404, detail="Paciente no encontrado")

#     try:
#         return Patient(**patient_schema(raw_patient))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error al procesar el paciente: {str(e)}")



@router.get("/{patient_id}/medical_history", summary="Obtener historial médico de un paciente", response_description="Historial médico")
def get_medical_history(patient_id: str):
    """
    Obtiene todas las entradas del historial médico del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.

    Retorna:
    - Lista de entradas del historial médico.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    patient = patients_collection.find_one({"_id": object_id})
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente no encontrado")

    medical_history = patient.get("medical_history", [])

    return medical_history_schema(medical_history)


@router.put("/{patient_id}/medical_history", summary="Actualizar un registro del historial médico de un paciente", response_description="Registro del historial médico actualizado")
def update_medical_history_entry(patient_id: str, updated_entry: MedicalHistoryEntry):
    """
    Actualiza un registro específico del historial médico del paciente especificado.

    Parámetros:
    - patient_id: ID del paciente.
    - updated_entry (en el body): Registro completo de historial médico. Se usará el campo `date` como identificador.

    Retorna:
    - Mensaje de éxito si el registro fue actualizado.
    - Error 404 si no se encontró el registro a actualizar.
    """
    try:
        object_id = ObjectId(patient_id)
    except bson_errors.InvalidId:
        raise HTTPException(status_code=400, detail="Formato de patient_id inválido")

    updated_datetime = updated_entry.date

    updated_entry_dict = updated_entry.dict()
    updated_entry_dict["date"] = updated_datetime

    result = patients_collection.update_one(
        {"_id": object_id, "medical_history.date": updated_datetime},
        {"$set": {"medical_history.$": updated_entry_dict}}
    )

    if result.modified_count == 1:
        return {"message": "Registro del historial médico actualizado exitosamente"}

    raise HTTPException(status_code=404, detail="No se encontró el registro a actualizar")