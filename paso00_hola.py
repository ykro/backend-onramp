"""Paso 0 (~35 min): tu primer servidor web con FastAPI.

Levanta el servidor con `uv run uvicorn paso00_hola:app --reload`, ábrelo en el navegador
(`http://127.0.0.1:8000/` y `http://127.0.0.1:8000/docs`) y resuelve los TODO hasta que pase
`uv run onramp check --paso 0`.
"""

from fastapi import FastAPI

app = FastAPI(title="Biblioteca Onramp - Paso 0")

LIBROS: list[dict[str, object]] = [
    {"id": 1, "titulo": "El Señor Presidente", "anio": 1946},
    {"id": 2, "titulo": "Hombres de Maíz", "anio": 1949},
]


@app.get("/")
def raiz() -> dict[str, str]:
    """Responde un JSON fijo para comprobar que el servidor está vivo."""
    return {"mensaje": "Hola desde la biblioteca"}


# TODO 1: Hoy `GET /saludo/Ana` responde 404 porque esa ruta no existe.
# Debe responder 200 con {"saludo": "Hola, Ana"}, con el nombre que venga en la URL.

# TODO 2: Hoy `GET /libros` responde 404. Debe responder 200 con la lista `LIBROS` en JSON.
