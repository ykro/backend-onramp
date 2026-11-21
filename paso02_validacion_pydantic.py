"""Paso 2 (~10 min): Validación estricta con Pydantic, `extra="forbid"` y `Decimal`.

Corre `uv run onramp inspect --paso 2` para ver qué acepta hoy el servidor y luego
corrige los TODO de `BookCreate` hasta que pase `uv run onramp check --paso 2`.
"""

from decimal import Decimal

from fastapi import FastAPI, status
from pydantic import BaseModel, ConfigDict, Field


class BookCreate(BaseModel):
    """Datos de entrada para registrar un libro en el catálogo."""

    # TODO 1: Agrega `model_config = ConfigDict(extra="forbid")` para rechazar campos extra con 422.
    # TODO 2: Restringe `title` con `Field(min_length=1, max_length=120)`.
    # TODO 3: Cambia `price` de `float` a `Decimal` con `Field(gt=Decimal("0"), decimal_places=2)`.
    title: str
    price: float


class BookOut(BaseModel):
    """Representación pública de un libro registrado."""

    id: int
    title: str
    price: Decimal


def create_app() -> FastAPI:
    """Crea una aplicación FastAPI enfocada en validar la entrada con Pydantic."""
    app = FastAPI(title="Biblioteca Onramp - Paso 2")
    books: dict[int, BookOut] = {}
    next_id = 1

    @app.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
    def create_book(payload: BookCreate) -> BookOut:
        nonlocal next_id
        book = BookOut(id=next_id, title=payload.title, price=Decimal(str(payload.price)))
        books[next_id] = book
        next_id += 1
        return book

    # Referencias disponibles para los TODO de este archivo.
    _ = (ConfigDict, Field)
    return app
