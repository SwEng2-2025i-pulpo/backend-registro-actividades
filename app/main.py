from fastapi import FastAPI, Request
from fastapi.responses import Response
from fastapi.middleware.cors import CORSMiddleware
from app.routers import caretakers, patients
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

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

# Métricas Prometheus
REQUEST_COUNT = Counter(
    "http_requests_total", "Total de peticiones HTTP", ["method", "endpoint", "http_status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds", "Duración de la petición en segundos", ["method", "endpoint"]
)

EXCEPTIONS_COUNT = Counter(
    "http_exceptions_total", "Conteo de excepciones por endpoint", ["method", "endpoint"]
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    method = request.method
    endpoint = request.url.path

    try:
        response = await call_next(request)
        status_code = response.status_code
    except Exception:
        EXCEPTIONS_COUNT.labels(method=method, endpoint=endpoint).inc()
        status_code = 500
        raise

    duration = time.time() - start_time
    REQUEST_COUNT.labels(method=method, endpoint=endpoint, http_status=status_code).inc()
    REQUEST_LATENCY.labels(method=method, endpoint=endpoint).observe(duration)

    return response


@app.get("/metrics")
def metrics():
    raw_metrics = generate_latest().decode('utf-8')
    resumen = {}

    for line in raw_metrics.splitlines():
        if line.startswith("http_requests_total{"):
            # Extraemos método, endpoint y valor
            partes = line.split()
            labels_part = partes[0]
            count = float(partes[1])

            # Extraer método y endpoint con parsing básico
            method = labels_part.split('method="')[1].split('"')[0]
            endpoint = labels_part.split('endpoint="')[1].split('"')[0]

            key = (endpoint, method)
            resumen[key] = resumen.get(key, 0) + count

    resumen_str = "\n# === Resumen total de peticiones por endpoint y método ===\n"
    for (endpoint, method), total in resumen.items():
        resumen_str += f"# Endpoint: {endpoint}, Method: {method}, Total: {int(total)}\n"

    # Resumen de latencias
    latencias = {}
    counts = {}

    for line in raw_metrics.splitlines():
        if line.startswith("http_request_duration_seconds_sum{"):
            parts = line.split()
            labels_part = parts[0]
            total_time = float(parts[1])

            method = labels_part.split('method="')[1].split('"')[0]
            endpoint = labels_part.split('endpoint="')[1].split('"')[0]

            latencias[(endpoint, method)] = total_time

        elif line.startswith("http_request_duration_seconds_count{"):
            parts = line.split()
            labels_part = parts[0]
            count = float(parts[1])

            method = labels_part.split('method="')[1].split('"')[0]
            endpoint = labels_part.split('endpoint="')[1].split('"')[0]

            counts[(endpoint, method)] = count

    latencia_str = "\n# === Latencia promedio por endpoint y método (en segundos) ===\n"
    for key in latencias:
        total_time = latencias.get(key, 0)
        count = counts.get(key, 1)
        promedio = total_time / count if count else 0
        latencia_str += f"# Endpoint: {key[0]}, Method: {key[1]}, Promedio: {promedio:.4f} segundos\n"

    # Resumen de errores

    errores = {}

    for line in raw_metrics.splitlines():
        if line.startswith("http_exceptions_total{"):
            parts = line.split()
            labels_part = parts[0]
            count = float(parts[1])

            method = labels_part.split('method="')[1].split('"')[0]
            endpoint = labels_part.split('endpoint="')[1].split('"')[0]

            errores[(endpoint, method)] = count

    errores_str = "\n# === Errores totales por endpoint y método ===\n"
    if errores:
        for key, count in errores.items():
            errores_str += f"# Endpoint: {key[0]}, Method: {key[1]}, Errores: {int(count)}\n"
    else:
        errores_str += "# No se registraron errores.\n"


    # Devolver las métricas con el resumen y latencias
    return Response(raw_metrics + "\n" + resumen_str + "\n" + latencia_str + "\n" + errores_str, media_type=CONTENT_TYPE_LATEST)


# uvicorn app.main:app --reload

