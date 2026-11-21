"""Paso 3 (~12 min): Depends, dependency_overrides, JWT en Base64Url y 401 vs 403.

Corre `uv run onramp inspect --paso 3` para observar cómo responden las rutas hoy
y completa los tres TODO hasta que pase `uv run onramp check --paso 3`.
"""

import base64
import json
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

JWT_SECRET = "clave-local-de-practica-32-bytes-segura"
JWT_ALGORITHM = "HS256"


class RoomCreate(BaseModel):
    """Datos de entrada para registrar una sala de estudio."""

    model_config = ConfigDict(extra="forbid")

    code: str = Field(min_length=1, max_length=40)
    name: str = Field(min_length=1, max_length=80)


class RoomRepository:
    """Almacén en memoria para salas de estudio."""

    def __init__(self, initial_rooms: list[dict[str, str]] | None = None) -> None:
        self._rooms: list[dict[str, str]] = (
            list(initial_rooms)
            if initial_rooms is not None
            else [{"code": "sala-a", "name": "Sala A"}]
        )

    def list_rooms(self) -> list[dict[str, str]]:
        return list(self._rooms)

    def add_room(self, code: str, name: str) -> dict[str, str]:
        room = {"code": code, "name": name}
        self._rooms.append(room)
        return room


_default_repo = RoomRepository()


def get_room_repo() -> RoomRepository:
    """Dependencia por defecto que devuelve el repositorio de salas."""
    return _default_repo


def create_access_token(subject: str, role: str) -> str:
    """Firma un JWT HS256 con el usuario y su rol."""
    return jwt.encode({"sub": subject, "role": role}, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_jwt_payload_unverified(token: str) -> dict[str, object]:
    """Decodifica el bloque central de un JWT usando Base64Url sin clave secreta."""
    # TODO 2: Separa `token` por `.`, toma el segundo segmento (índice 1), agrega el relleno `=`
    # faltante para que su longitud sea múltiplo de 4, decodifica con `base64.urlsafe_b64decode`
    # y convierte el JSON a diccionario con `json.loads`.
    _ = (base64, json, token)
    raise NotImplementedError("Completa la decodificación Base64Url del segmento central")


def _extract_bearer_token(authorization: str | None) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Falta el encabezado Authorization con Bearer token",
        )
    return authorization.removeprefix("Bearer ").strip()


def create_app() -> FastAPI:
    """Crea la aplicación FastAPI del Paso 3 con Depends y validación de JWT."""
    app = FastAPI(title="Biblioteca Onramp - Paso 3")

    @app.get("/rooms")
    def list_rooms() -> list[dict[str, str]]:
        # TODO 1: Inyecta el repositorio con `Annotated[RoomRepository, Depends(get_room_repo)]`
        # en lugar de usar `_default_repo` directo para que `dependency_overrides` funcione.
        _ = (Annotated, Depends)
        return _default_repo.list_rooms()

    @app.post("/admin/rooms", status_code=status.HTTP_201_CREATED)
    def create_room(
        payload: RoomCreate,
        repo: Annotated[RoomRepository, Depends(get_room_repo)],
        authorization: Annotated[str | None, Header()] = None,
    ) -> dict[str, str]:
        token = _extract_bearer_token(authorization)
        try:
            claims = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        except jwt.PyJWTError as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido o mal firmado",
            ) from exc

        if claims.get("role") != "librarian":
            # TODO 3: Aquí el usuario sí tiene un token válido, pero su rol no tiene permiso.
            # Cambia este código de 401 a 403 Forbidden.
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Se requiere rol librarian para crear salas",
            )

        return repo.add_room(code=payload.code, name=payload.name)

    return app
