# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

## [v1.1.2] - 2025-06-09

### Added
- Implementación del servicio **Registro Diario de Actividades**.
- Endpoints RESTful completos para:
  - `medication_logs` (POST, GET).
  - `meals` (POST, GET).
  - `hygiene_logs` (POST, GET).
  - `vital_signs` (POST, GET).
  - `symptoms` (POST, GET).
  - `medical_history` (POST, GET).
- Validación de modelos con **Pydantic** para todos los POST.
- Serialización de respuestas con schemas en `db/schemas/activity.py`.
- Documentación automática completa en `/docs` (OpenAPI).
- Conexión asíncrona con base de datos **MongoDB Atlas**.
- Soporte para múltiples pacientes (estructura preparada con `patient_id` en endpoints).

### Changed
- Refactorización del código para separar modelos (`db/models/activity.py`) y schemas de serialización.

### Notes
- La integración con el frontend se encuentra en etapa de pruebas.
- Actualmente el sistema trabaja con un paciente predefinido para pruebas.

---
