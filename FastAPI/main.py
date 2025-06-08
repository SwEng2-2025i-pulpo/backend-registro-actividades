from fastapi import FastAPI
from routers import caretakers, patients


app = FastAPI() # Inicializamos FastAPI

# Routers

app.include_router(caretakers.router) # Inicializamos la api desde router.
app.include_router(patients.router)



#uvicorn main:app --reload 