"""Paso 2 (~60 min): SQLite relacional, INNER JOIN, paginación segura e índices.

Corre `uv run onramp inspect --paso 2` para ver que SQLite permite llaves foráneas rotas y hace
`SCAN books` en lugar de usar un índice. Completa los TODO hasta pasar `--paso 2`.
"""

import sqlite3


def init_db(conn: sqlite3.Connection) -> None:
    """Activa llaves foráneas, crea las tablas authors y books y agrega el índice."""
    conn.row_factory = sqlite3.Row

    # TODO 1: Hoy SQLite guarda libros con un author_id que no existe, aunque la tabla declara
    # FOREIGN KEY. Esa verificación viene apagada en cada conexión nueva.

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            year INTEGER NOT NULL,
            author_id INTEGER NOT NULL,
            FOREIGN KEY (author_id) REFERENCES authors(id)
        )
        """
    )

    # TODO 4: Hoy buscar por author_id recorre toda la tabla (`SCAN books`). Crea el índice
    # `idx_books_author_id` para que la búsqueda use `SEARCH ... USING INDEX`.

    conn.commit()


def add_author(conn: sqlite3.Connection, name: str) -> int:
    """Inserta un autor y devuelve su identificador."""
    cursor = conn.execute("INSERT INTO authors (name) VALUES (?)", (name,))
    conn.commit()
    assert cursor.lastrowid is not None
    return int(cursor.lastrowid)


def add_book(conn: sqlite3.Connection, title: str, year: int, author_id: int) -> int:
    """Inserta un libro vinculado a un autor existente y devuelve su identificador."""
    cursor = conn.execute(
        "INSERT INTO books (title, year, author_id) VALUES (?, ?, ?)",
        (title, year, author_id),
    )
    conn.commit()
    assert cursor.lastrowid is not None
    return int(cursor.lastrowid)


def list_books_with_authors(conn: sqlite3.Connection) -> list[dict[str, object]]:
    """Devuelve todos los libros junto con el nombre de su autor usando INNER JOIN."""
    # TODO 2: Devuelve cada libro con el nombre de su autor, ordenados por id del libro.
    # Cada elemento es un diccionario con las llaves id, title, year y author_name.
    _ = conn
    return []


def list_books_page(
    conn: sqlite3.Connection,
    limit: int,
    offset: int,
    title_filter: str | None = None,
) -> list[dict[str, object]]:
    """Devuelve una página ordenada de libros usando parámetros '?' seguros."""
    # TODO 3: Devuelve una página de libros (con author_name) ordenada por título: `limit` filas
    # a partir de la fila `offset`. Si `title_filter` trae texto, solo títulos que lo contengan.
    # El texto del usuario nunca se pega dentro del SQL.
    _ = (conn, limit, offset, title_filter)
    return []


def explain_books_by_author(conn: sqlite3.Connection, author_id: int) -> list[str]:
    """Devuelve el detalle de EXPLAIN QUERY PLAN al buscar libros por author_id."""
    rows = conn.execute(
        "EXPLAIN QUERY PLAN SELECT id, title FROM books WHERE author_id = ?",
        (author_id,),
    ).fetchall()
    return [str(row["detail"]) for row in rows]
