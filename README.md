# Backend On-Ramp (60 minutos)

Este repositorio te prepara en una hora para tomar el [Curso 1 de Backend con FastAPI](https://github.com/ykro/backend-course). Trabajarás con el dominio de una biblioteca pequeña (libros, autores y reservas de salas de estudio) usando solo Python y SQLite en memoria, sin Docker y sin cuentas externas.

**Repositorios relacionados**

- Índice general de nivelaciones: [ykro/courses-onramp](https://github.com/ykro/courses-onramp)
- Curso principal: [ykro/backend-course](https://github.com/ykro/backend-course)
- Solución de referencia explicada paso a paso: [ykro/backend-onramp-solution](https://github.com/ykro/backend-onramp-solution)

## Instalación

Necesitas `uv` instalado en tu computadora. En la raíz del repositorio corre:

```bash
uv sync
```

Si `uv` reporta un problema de permisos con la caché global, usa una caché temporal:

```bash
UV_CACHE_DIR=/tmp/uv-cache-onramp uv sync
```

## Cómo trabajar los ejercicios

1. Corre el inspector para ver en vivo qué devuelve cada módulo hoy (peticiones HTTP crudas, plan de consulta de SQLite y simulación de concurrencia):

```bash
uv run onramp inspect
```

2. Corre el verificador para ver qué pruebas pasan y cuáles fallan:

```bash
uv run onramp check
```

3. Resuelve un archivo a la vez siguiendo la guía paso a paso de abajo:
   - [lab01_http_y_servidor.py](./lab01_http_y_servidor.py) (~20 min)
   - [lab02_sql_relacional.py](./lab02_sql_relacional.py) (~20 min)
   - [lab03_di_jwt_y_carrera.py](./lab03_di_jwt_y_carrera.py) (~20 min)
4. Después de cada cambio, corre `uv run onramp inspect` y `uv run onramp check` hasta que pasen las 12 pruebas de [tests/test_onramp.py](./tests/test_onramp.py).

---

## Guía paso a paso por laboratorio

Si en algún paso dices *"no entiendo"*, abre el enlace oficial del concepto antes de tocar el código. Cada enlace apunta a la documentación original de MDN, FastAPI, Pydantic, Python o SQLite.

### Lab 1: HTTP, validación estricta y estado aislado

Archivo: [lab01_http_y_servidor.py](./lab01_http_y_servidor.py)

Este servidor recibe libros en memoria con [FastAPI](https://fastapi.tiangolo.com/), pero comete cuatro errores comunes de un backend inicial.

1. **TODO 1 — Valida la entrada en `BookCreate`**:
   - Agrega `model_config = ConfigDict(extra="forbid")` para rechazar campos que el cliente no debería enviar. Lee [Pydantic `ConfigDict`](https://docs.pydantic.dev/latest/api/config/).
   - Restringe `title` con `Field(min_length=1, max_length=120)` para impedir títulos vacíos. Lee [Pydantic `Field`](https://docs.pydantic.dev/latest/concepts/fields/).
   - Cambia `price` de `float` a `Decimal` con `Field(gt=Decimal("0"), decimal_places=2)` para evitar errores de redondeo en dinero y rechazar precios negativos o cero. Lee [Python `Decimal`](https://docs.python.org/3/library/decimal.html).
2. **TODO 2 — Devuelve `201 Created` en `POST /books`**:
   - Pasa `status_code=status.HTTP_201_CREATED` al decorador `@app.post("/books", ...)`. Lee [FastAPI Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/) y [HTTP status codes en MDN](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status).
3. **TODO 3a y 3b — Corrige `404 Not Found` y `204 No Content`**:
   - En `GET /books/{book_id}`, cuando el libro no existe, lanza `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")` en vez de devolver un diccionario con código `200`. Lee [FastAPI Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/).
   - En `DELETE /books/{book_id}`, agrega `status_code=status.HTTP_204_NO_CONTENT` y devuelve `Response(status_code=status.HTTP_204_NO_CONTENT)` para responder sin cuerpo.
4. **TODO 4 — Aísla el estado dentro de `create_app()`**:
   - Elimina `_SHARED_BOOKS` y `_NEXT_ID` del nivel de módulo y decláralos como variables locales (`books` y `next_id`) dentro de `create_app()`, usando `nonlocal next_id` en `create_book`. Así dos instancias de la aplicación nunca mezclan sus datos.

### Lab 2: SQLite relacional, JOIN, paginación e índices

Archivo: [lab02_sql_relacional.py](./lab02_sql_relacional.py)

Aquí trabajas directo con el módulo [`sqlite3`](https://docs.python.org/3/library/sqlite3.html) de Python, sin ORM, para ver cómo responde una base de datos relacional real.

1. **TODO 1 — Activa llaves foráneas en `init_db`**:
   - SQLite desactiva las llaves foráneas por defecto en cada conexión nueva. Ejecuta `conn.execute("PRAGMA foreign_keys = ON")` antes de crear las tablas para que SQLite lance `sqlite3.IntegrityError` si alguien intenta insertar un libro con un `author_id` inexistente. Lee [SQLite `PRAGMA foreign_keys`](https://www.sqlite.org/foreignkeys.html).
2. **TODO 2 — Une tablas con `INNER JOIN` en `list_books_with_authors`**:
   - Consulta `books AS b` unido con `authors AS a ON a.id = b.author_id`, ordena con `ORDER BY b.id ASC` y devuelve una lista de diccionarios con las llaves `id`, `title`, `year` y `author_name`. Lee [SQLite `INNER JOIN`](https://www.sqlite.org/lang_select.html#fromclause).
3. **TODO 3 — Pagina y filtra con parámetros `?` en `list_books_page`**:
   - Usa `ORDER BY b.title ASC LIMIT ? OFFSET ?` con el mismo `INNER JOIN` a `authors`.
   - Si `title_filter` no es `None`, agrega `WHERE b.title LIKE ?` y pasa `f"%{title_filter}%"` como parámetro en la tupla de `conn.execute(...)`. Nunca concatenes texto del usuario dentro del string SQL. Lee [SQLite `ORDER BY`](https://www.sqlite.org/lang_select.html#orderby) y [SQLite `LIMIT` / `OFFSET`](https://www.sqlite.org/lang_select.html#limitoffset).
4. **TODO 4 — Crea un índice en `init_db` para eliminar el escaneo completo**:
   - Ejecuta `CREATE INDEX IF NOT EXISTS idx_books_author_id ON books(author_id)`.
   - Corre `uv run onramp inspect` y verifica que `EXPLAIN QUERY PLAN` cambie de `SCAN books` a `SEARCH books USING INDEX idx_books_author_id`. Lee [SQLite `EXPLAIN QUERY PLAN`](https://www.sqlite.org/eqp.html).

### Lab 3: Inyección de dependencias, JWT y condición de carrera

Archivo: [lab03_di_jwt_y_carrera.py](./lab03_di_jwt_y_carrera.py)

Este laboratorio reúne tres piezas clave de cualquier API en producción: dependencias reemplazables en pruebas, autenticación/autorización con JWT y acceso concurrente a memoria compartida.

1. **TODO 1 — Inyecta el repositorio con `Depends` en `GET /rooms`**:
   - Cambia la firma de `list_rooms` para recibir `repo: Annotated[RoomRepository, Depends(get_room_repo)]` y retorna `repo.list_rooms()` en lugar de leer `_default_repo` directo. Así `app.dependency_overrides[get_room_repo]` puede sustituir el repositorio en las pruebas. Lee [FastAPI `Depends`](https://fastapi.tiangolo.com/tutorial/dependencies/) y [`dependency_overrides`](https://fastapi.tiangolo.com/advanced/testing-dependencies/).
2. **TODO 2 — Decodifica el segmento central de un JWT en `decode_jwt_payload_unverified`**:
   - Un JWT tiene tres bloques separados por punto: `encabezado.contenido.firma`. El bloque central no está cifrado, solo codificado en Base64Url.
   - Separa `token.split(".")`, toma `parts[1]`, agrega el relleno `=` faltante (`"=" * (-len(payload_segment) % 4)`), decodifica con `base64.urlsafe_b64decode(...)` y convierte el JSON con `json.loads(...)`. Lee [RFC 7519 (JWT)](https://datatracker.ietf.org/doc/html/rfc7519) y [Python `base64.urlsafe_b64decode`](https://docs.python.org/3/library/base64.html#base64.urlsafe_b64decode).
3. **TODO 3 — Separa `401` de `403` en `POST /admin/rooms`**:
   - Cuando falta el token o la firma falla, el código correcto es `401 Unauthorized` (no sabemos quién eres).
   - Cuando el token es válido pero `claims.get("role") != "librarian"`, el código correcto es `403 Forbidden` (sabemos quién eres, pero tu rol no tiene permiso). Cambia `status.HTTP_401_UNAUTHORIZED` por `status.HTTP_403_FORBIDDEN`. Lee [MDN `401 Unauthorized`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401) frente a [MDN `403 Forbidden`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403).
4. **TODO 4 — Protege la reserva concurrente con `threading.Lock`**:
   - En `RoomReservationService.__init__`, crea `self._lock = threading.Lock()`.
   - Envuelve el cuerpo de `reserve` y `reservation_count` dentro de `with self._lock:`. Así solo un hilo a la vez revisa si la sala está libre y guarda la reserva. Lee [Python `threading.Lock`](https://docs.python.org/3/library/threading.html#lock-objects).

---

## Glosario con documentación oficial

| Concepto | Qué resuelve en este repositorio | Documentación oficial |
| :--- | :--- | :--- |
| **HTTP status codes** | Diferenciar creación (`201`), borrado sin cuerpo (`204`), recurso ausente (`404`) y error de validación (`422`). | [MDN HTTP response status codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) |
| **FastAPI** | Definir rutas HTTP, serializar respuestas y validar datos de entrada en Python. | [FastAPI Documentation](https://fastapi.tiangolo.com/) |
| **Pydantic `Field` y `ConfigDict`** | Imponer restricciones en campos (`min_length`, `gt`, `decimal_places`) y prohibir campos extra (`extra="forbid"`). | [Pydantic Fields](https://docs.pydantic.dev/latest/concepts/fields/) · [Pydantic ConfigDict](https://docs.pydantic.dev/latest/api/config/) |
| **Python `Decimal`** | Representar precios exactos en base 10 sin errores de punto flotante binario (`float`). | [Python `decimal` module](https://docs.python.org/3/library/decimal.html) |
| **SQLite `PRAGMA foreign_keys`** | Activar la verificación de integridad referencial para impedir filas huérfanas. | [SQLite Foreign Key Support](https://www.sqlite.org/foreignkeys.html) |
| **`INNER JOIN`** | Combinar filas relacionadas de `books` y `authors` en una sola consulta SQL. | [SQLite `SELECT` y `JOIN`](https://www.sqlite.org/lang_select.html#fromclause) |
| **`ORDER BY` / `LIMIT` / `OFFSET`** | Ordenar resultados de forma predecible y devolver una página acotada con parámetros `?`. | [SQLite `ORDER BY`](https://www.sqlite.org/lang_select.html#orderby) · [SQLite `LIMIT` / `OFFSET`](https://www.sqlite.org/lang_select.html#limitoffset) |
| **`EXPLAIN QUERY PLAN`** | Inspeccionar si SQLite recorre toda la tabla (`SCAN`) o busca directo en un índice (`SEARCH USING INDEX`). | [SQLite `EXPLAIN QUERY PLAN`](https://www.sqlite.org/eqp.html) |
| **FastAPI `Depends`** | Declarar qué repositorio o recurso necesita una ruta sin acoplarla a una variable global. | [FastAPI Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) |
| **`dependency_overrides`** | Sustituir una dependencia real por un repositorio en memoria aislado durante las pruebas. | [FastAPI Testing Dependencies](https://fastapi.tiangolo.com/advanced/testing-dependencies/) |
| **JWT y `Base64Url`** | Firmar y verificar tokens de sesión (`HS256`) y comprobar que su bloque central es legible sin clave secreta. | [RFC 7519 (JWT)](https://datatracker.ietf.org/doc/html/rfc7519) · [PyJWT](https://pyjwt.readthedocs.io/en/stable/) · [Python `urlsafe_b64decode`](https://docs.python.org/3/library/base64.html#base64.urlsafe_b64decode) |
| **`401` frente a `403`** | Separar falta de identidad o token inválido (`401`) de falta de permisos para un usuario autenticado (`403`). | [MDN `401 Unauthorized`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/401) · [MDN `403 Forbidden`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/403) |
| **`threading.Lock`** | Garantizar exclusión mutua para evitar que dos hilos reserven la misma sala al mismo tiempo. | [Python `threading.Lock`](https://docs.python.org/3/library/threading.html#lock-objects) |

## Uso de IA

Puedes usar tu asistente de IA con libertad mientras resuelves estos ejercicios. El archivo [AGENTS.md](./AGENTS.md) configura al asistente en modo tutor socrático para que te explique cada concepto, te dé pistas progresivas y te ayude a leer las respuestas del servidor sin quitarte la oportunidad de entender qué ocurre en cada línea.
