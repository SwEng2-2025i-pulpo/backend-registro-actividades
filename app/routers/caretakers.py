from fastapi import APIRouter, HTTPException
from app.db.models.caretaker import Caretaker
from app.db.client import db_client
from app.db.schemas.caretaker import caretaker_schema, caretakers_schema
from bson import ObjectId

# en este archivo deben ir los métodos para trabajar con la base de datos (get, post, put, delete)

router = APIRouter(prefix="/caretakers", tags=["caretakers"]) # Inicializamos la ruta para que main la reconozca e inicialice FastAPI

#Métodos para caretaker

@router.post("/", response_model=Caretaker, status_code=201) # crear caretaker
async def caretaker(user: Caretaker):

    if type(search_caretakers(user.email)) == Caretaker: 
        raise HTTPException(status_code=206, detail="El correo ya existe")

    user_dict = dict(user)

    del user_dict["id"] # eliminamos el id porque mongo lo asigna automáticamente

    ide = db_client.conectacare.caretaker.insert_one(user_dict).inserted_id

    new_user= caretaker_schema(db_client.conectacare.caretaker.find_one({"_id": ide}))

    return Caretaker(**new_user)




@router.get("/", response_model=list[Caretaker]) # muestra todos los caretakers
async def caretakers():
    return caretakers_schema(db_client.conectacare.caretaker.find())

@router.get("/{id}", response_model=Caretaker)
async def caretakerid(id:str):
    return search_caretakersid("_id", ObjectId(id))

def search_caretakersid(field: str, key): # función para obtener un caretaker
    try:
        duplicate = caretaker_schema(db_client.conectacare.caretaker.find_one({field: key}))
        return Caretaker(**duplicate)
    except:
        return {"error": "no se ha encontrado el usuario getbyid"}


def search_caretakers(email:str): # función para verificar emails duplicados
    try:
        duplicate = caretaker_schema(db_client.conectacare.caretaker.find_one({"email":email}))
        return Caretaker(**duplicate)
    except:
        return {"error": "no se ha encontrado el usuario"}
    
    