# Biblioteca — Backend Onramp

Este repositorio es un **onramp** práctico y autoevaluable de 60 minutos para preparar tu entrada al [Curso 1 de Backend con FastAPI](https://github.com/ykro/backend-course). Todo gira alrededor de una biblioteca pequeña (libros, autores y salas de estudio) usando solo Python y SQLite en memoria, sin Docker y sin cuentas externas. Cada uno de los cinco pasos se puede trabajar y verificar de forma independiente: si ya dominas HTTP y Pydantic, puedes arrancar directo en el Paso 3, el 4 o el 5.

![Mapa general de Backend Onramp](docs/diagrams/overview.svg)

## Los 5 pasos (independientes)

| Paso | Enfoque | Archivo | Guía |
| --- | --- | --- | --- |
| Paso 1 | Contratos HTTP/1.1 (`201`, `204`, `404`) y estado aislado por instancia | [paso01_http_contratos.py](paso01_http_contratos.py) | [steps/01-http-contratos/README.md](steps/01-http-contratos/README.md) |
| Paso 2 | Validación estricta con Pydantic (`extra="forbid"`, `Decimal` y `422`) | [paso02_validacion_pydantic.py](paso02_validacion_pydantic.py) | [steps/02-validacion-pydantic/README.md](steps/02-validacion-pydantic/README.md) |
| Paso 3 | SQLite relacional (`PRAGMA foreign_keys`, `INNER JOIN`, paginación e índice) | [paso03_sql_relacional.py](paso03_sql_relacional.py) | [steps/03-sql-relacional/README.md](steps/03-sql-relacional/README.md) |
| Paso 4 | `Depends`, `dependency_overrides`, JWT en Base64Url y `401` vs `403` | [paso04_depends_y_jwt.py](paso04_depends_y_jwt.py) | [steps/04-depends-y-jwt/README.md](steps/04-depends-y-jwt/README.md) |
| Paso 5 | Concurrencia y exclusión mutua con `threading.Lock` ante `Barrier(5)` | [paso05_concurrencia.py](paso05_concurrencia.py) | [steps/05-concurrencia/README.md](steps/05-concurrencia/README.md) |

## Inicio rápido

1. Clona este repositorio en local con Python 3.13 y `uv`.
2. Instala las dependencias en la raíz del proyecto con `uv sync` (si `uv` reporta permisos en la caché global, usa `UV_CACHE_DIR=/tmp/uv-cache-onramp uv sync`).
3. Elige el paso por donde quieras empezar y observa cómo responde hoy el código con `uv run onramp inspect --paso N` (o `uv run onramp inspect` para ver los 5 pasos).
4. Edita el archivo del paso siguiendo su guía en `steps/0N-.../README.md`.
5. Valida tu avance por paso con `uv run onramp check --paso N` o corre las 15 pruebas completas con `uv run onramp check`.

Si algún término resulta nuevo, consulta el [glosario con documentación oficial](docs/glosario.md). Puedes usar tu asistente de IA con libertad mientras resuelves cada paso: [AGENTS.md](AGENTS.md) lo configura en modo tutor socrático para explicar conceptos y darte pistas progresivas.

## Repositorios relacionados

- Índice general de nivelaciones: [ykro/courses-onramp](https://github.com/ykro/courses-onramp)
- Curso principal: [ykro/backend-course](https://github.com/ykro/backend-course)
- Solución de referencia explicada paso a paso: [ykro/backend-onramp-solution](https://github.com/ykro/backend-onramp-solution)
