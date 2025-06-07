from pydantic import BaseModel
# En este archivo se hace la clase base del caretaker y los atributos que contiene.
class Caretaker (BaseModel):
    
    id: int
    name: str
