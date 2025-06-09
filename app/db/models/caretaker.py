from pydantic import BaseModel
# En este archivo se hace la clase base del caretaker y los atributos que contiene.
class Caretaker (BaseModel):
    
    id: str | None = None # puede ser opcional porque mongo asigna id's automaticos
    name: str
    email: str
    passwordHash: str
    role: str
