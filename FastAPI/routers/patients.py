from fastapi import APIRouter, HTTPException
from db.models.patient import Patient
# en este archivo deben ir los métodos para trabajar con la base de datos (get, post, put, delete)

router = APIRouter(prefix="/patients", tags=["patients"])


@router.get("/")
async def patients():
    return "holi"
