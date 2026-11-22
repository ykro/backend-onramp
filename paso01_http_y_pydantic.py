"""Paso 1 (~40 min): Contratos HTTP/1.1 (201, 204, 404), estado aislado y validación Pydantic.

Corre `uv run onramp inspect --paso 1` para ver las respuestas actuales del servidor y luego
corrige los TODO de este archivo hasta que pase `uv run onramp check --paso 1`.
"""

from decimal import Decimal

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field

# TODO 1: Estos dos valores viven fuera de `create_app()`, así que dos apps creadas con
# `create_app()` comparten los mismos libros. Cada app debe tener su propio catálogo.
_SHARED_BOOKS: dict[int, "BookOut"] = {}
_NEXT_ID = 1


class BookCreate(BaseModel):
    """Datos de entrada para registrar un libro en el catálogo."""

    # TODO 2: Hoy se aceptan campos que el modelo no conoce. Deben rechazarse con 422.
    # TODO 3: Hoy el título puede venir vacío y el precio es float (acepta cero, negativos y
    # más de dos decimales). El título lleva de 1 a 120 caracteres y el precio debe ser exacto
    # en base 10, mayor que cero y con dos decimales como máximo.
    title: str
    price: float


class BookOut(BaseModel):
    """Representación pública de un libro registrado."""

    id: int
    title: str
    price: Decimal


def create_app() -> FastAPI:
    """Crea una aplicación FastAPI con su propio catálogo en memoria y validación estricta."""
    app = FastAPI(title="Biblioteca Onramp - Paso 1")

    # TODO 4: Hoy POST /books responde 200. Un recurso recién creado responde 201.
    @app.post("/books", response_model=BookOut)
    def create_book(payload: BookCreate) -> BookOut:
        global _NEXT_ID
        book = BookOut(id=_NEXT_ID, title=payload.title, price=Decimal(str(payload.price)))
        _SHARED_BOOKS[_NEXT_ID] = book
        _NEXT_ID += 1
        return book

    @app.get("/books", response_model=list[BookOut])
    def list_books() -> list[BookOut]:
        return list(_SHARED_BOOKS.values())

    @app.get("/books/{book_id}")
    def get_book(book_id: int) -> dict[str, object] | BookOut:
        book = _SHARED_BOOKS.get(book_id)
        if book is None:
            # TODO 5: Hoy un libro inexistente responde 200 con un diccionario. Debe ser 404.
            return {"detail": "Libro no encontrado"}
        return book

    @app.delete("/books/{book_id}")
    def delete_book(book_id: int) -> dict[str, object]:
        if book_id not in _SHARED_BOOKS:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Libro no encontrado",
            )
        del _SHARED_BOOKS[book_id]
        # TODO 6: Hoy DELETE responde 200 con cuerpo JSON. Un borrado exitoso es 204 sin cuerpo.
        return {"deleted": book_id}

    # Referencias disponibles para los TODO de este archivo.
    _ = (ConfigDict, Field, Response)
    return app
