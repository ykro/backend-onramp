"""Paso 1 (~14 min): Contratos HTTP/1.1 (201, 204, 404), estado aislado y validación Pydantic.

Corre `uv run onramp inspect --paso 1` para ver las respuestas actuales del servidor y luego
corrige los TODO de este archivo hasta que pase `uv run onramp check --paso 1`.
"""

from decimal import Decimal

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, ConfigDict, Field

# TODO 4: Este diccionario global hace que dos instancias de `create_app()` compartan libros.
# Mueve el almacenamiento y el contador dentro de `create_app()` para aislar cada instancia.
_SHARED_BOOKS: dict[int, "BookOut"] = {}
_NEXT_ID = 1


class BookCreate(BaseModel):
    """Datos de entrada para registrar un libro en el catálogo."""

    # TODO 5: Agrega `model_config = ConfigDict(extra="forbid")` para rechazar campos extra con 422.
    # TODO 6: Restringe `title` con `Field(min_length=1, max_length=120)` y cambia `price` de
    # `float` a `Decimal` con `Field(gt=Decimal("0"), decimal_places=2)`.
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

    # TODO 1: Cambia el código de estado de POST /books a 201 Created.
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
            # TODO 2: Cuando el libro no existe, lanza HTTPException con código 404.
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
        # TODO 3: DELETE debe responder 204 No Content y sin cuerpo (`Response(status_code=204)`).
        return {"deleted": book_id}

    # Referencias disponibles para los TODO de este archivo.
    _ = (ConfigDict, Field, Response)
    return app
