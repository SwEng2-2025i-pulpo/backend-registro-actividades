# Backend - Módulo de Registro Diario de Actividades  
Proyecto **ConectaCare** - Ingeniería de Software II  
Universidad Nacional de Colombia - 2025-I

## 📌 Descripción del servicio

Este servicio backend corresponde al **Módulo de Registro Diario de Actividades** del sistema ConectaCare.

Su objetivo es permitir el **registro y consulta de actividades diarias** relacionadas con el cuidado de pacientes, incluyendo:

- Administración de medicación
- Ingesta de comidas
- Actividades de higiene
- Registro de signos vitales
- Reporte de síntomas
- Historial médico

El servicio expone una API RESTful para facilitar la integración con el frontend del sistema.

---

## ⚙️ Stack utilizado

- Lenguaje: **Python 3.12**  
- Framework: **FastAPI**  
- Base de datos: **MongoDB Atlas**  
- Librerías:
  - `pydantic` → modelos de validación de datos
  - `pymongo` → conexión con MongoDB
  - `bson` → manejo de ObjectId
- Documentación automática: **OpenAPI** (accesible vía `/docs`)

---

## 🚀 Endpoints implementados

Todos los endpoints siguen el patrón:

/patients/{patient_id}/...

👉 Se espera que el `patient_id` sea un **ObjectId** válido de MongoDB.

### Administración de medicación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST   | `/patients/{patient_id}/medication_logs` | Registrar administración de medicación |
| GET    | `/patients/{patient_id}/medication_logs` | Obtener registros de medicación |

### Ingesta de comidas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST   | `/patients/{patient_id}/meals` | Registrar comida |
| GET    | `/patients/{patient_id}/meals` | Obtener registros de comidas |

### Actividades de higiene

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST   | `/patients/{patient_id}/hygiene_logs` | Registrar actividad de higiene |
| GET    | `/patients/{patient_id}/hygiene_logs` | Obtener registros de higiene |

### Signos vitales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST   | `/patients/{patient_id}/vital_signs` | Registrar signos vitales |
| GET    | `/patients/{patient_id}/vital_signs` | Obtener registros de signos vitales |

### Síntomas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST   | `/patients/{patient_id}/symptoms` | Registrar síntoma |
| GET    | `/patients/{patient_id}/symptoms` | Obtener registros de síntomas |

### Historial médico

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST   | `/patients/{patient_id}/medical_history` | Registrar entrada en historial médico |
| GET    | `/patients/{patient_id}/medical_history` | Obtener historial médico |

---

## 🗂️ Modelos de datos

Todos los modelos de datos son validados usando **Pydantic**.

### Ejemplo: `medication_logs`

```json
{
  "datetime": "2025-06-08T08:30:00.000Z",
  "medication_name": "enalapril",
  "dose": "10mg",
  "route": "oral",
  "status": "administrado",
  "observations": "sin efectos adversos"
}
```

👉 Los demás modelos (meals, hygiene_logs, vital_signs, symptoms, medical_history) siguen una estructura similar → ver /docs para ejemplos completos.

## 🚧 Cómo probar el servicio
Ejecutar el backend:

```bash
uvicorn app.main:app --reload
```

Acceder a la documentación interactiva en:

```bash
http://127.0.0.1:8000/docs
```
Probar los endpoints usando /docs o herramientas como Postman o curl.

Para las pruebas se requiere un patient_id válido (actualmente la base contiene un paciente predefinido para pruebas).

## ⚠️ Consideraciones técnicas

El campo datetime y date son convertidos automáticamente a tipo Date en MongoDB → los valores deben ser enviados como ISO 8601 strings.

El backend valida automáticamente todos los datos con Pydantic.

La API es asíncrona y puede escalar para múltiples pacientes en futuras versiones.