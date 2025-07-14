import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URI de conexión desde las variables de entorno
mongo_uri = os.getenv('MONGO_URI')

# Verificar que la variable de entorno esté configurada
if not mongo_uri:
    raise ValueError("No se ha configurado MONGO_URI en las variables de entorno")

# Crear la conexión a MongoDB
try:
    db_client = MongoClient(mongo_uri)
    print("Conexión a MongoDB establecida correctamente")
except Exception as e:
    print(f"Error al conectar a MongoDB: {e}")
    raise