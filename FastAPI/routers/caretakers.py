from fastapi import APIRouter, HTTPException
from FastAPI.db.models.caretaker import Caretaker
from db.client import db_client 
# en este archivo deben ir los métodos para trabajar con la base de datos (get, post, put, delete)

router = APIRouter(prefix="/caretakers", tags=["caretakers"]) # Inicializamos la ruta para que main la reconozca e inicialice FastAPI


@router.get("/")

async def caretakers():
    return 




