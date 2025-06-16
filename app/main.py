from fastapi import FastAPI
from app.routers import caretakers, patients
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() # Inicializamos FastAPI

# Routers

app.include_router(caretakers.router) # Inicializamos la api desde router.
app.include_router(patients.router)


# Configuración de CORS
origins = [
    "http://localhost:3000",  # React local
    "http://localhost:5173",
    # Añadir otros orígenes aquí, como el dominio en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Origenes permitidos
    allow_credentials=True,
    allow_methods=["*"],    # Métodos permitidos
    allow_headers=["*"],    # Encabezados permitidos
)


# uvicorn app.main:app --reload
