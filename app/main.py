from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import caretakers, patients

app = FastAPI()  # Inicializamos FastAPI

# Configuración de CORS (esto debe estar antes de incluir los routers)
origins = [
    "http://localhost:3000",  # React local
    "http://localhost:5173",
    # Añadir otros orígenes aquí, como el dominio en producción
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # Orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],          # Métodos permitidos (GET, POST, etc.)
    allow_headers=["*"],          # Encabezados permitidos
)

# Routers
app.include_router(caretakers.router)
app.include_router(patients.router)


# uvicorn app.main:app --reload
