from pydantic import BaseModel
# En este archivo se hace la clase base del patient y los atributos que contiene
class Patient(BaseModel):

    id: str | None # volvemos el id opcional porque mongo lo pone automaticamente lo ponemos str porque mongo trabaja así
    name: str
    age: int

