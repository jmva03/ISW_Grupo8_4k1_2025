import pytest
from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import Session
from datetime import datetime
from pathlib import Path

# --- Configuración del engine temporal (en memoria) ---
# Usamos una base SQLite temporal para testing
engine = create_engine("sqlite:///:memory:", echo=False, future=True)

# Habilitar claves foráneas en SQLite
@event.listens_for(engine, "connect")
def _enable_sqlite_fk(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()


# --- Scripts DDL idénticos a los de la base real ---
DDL_SCRIPT = """
CREATE TABLE IF NOT EXISTS actividad (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL UNIQUE,
  requiere_talla INTEGER NOT NULL DEFAULT 0,
  cupos_maximos INTEGER NOT NULL,
  edad_minima INTEGER
);

CREATE TABLE IF NOT EXISTS turno (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  actividad_id INTEGER NOT NULL REFERENCES actividad(id),
  inicio TEXT NOT NULL,
  fin TEXT NOT NULL,
  estado TEXT NOT NULL DEFAULT 'abierto',
  cupos_disponibles INTEGER NOT NULL,
  fecha TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS reserva (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  turno_id INTEGER NOT NULL REFERENCES turno(id),
  cantidad_personas INTEGER NOT NULL,
  estado TEXT NOT NULL DEFAULT 'pendiente',
  tyc_aceptados INTEGER NOT NULL DEFAULT 0,
  creada_en DATETIME NOT NULL
);

CREATE TABLE IF NOT EXISTS reserva_participante (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  reserva_id INTEGER NOT NULL REFERENCES reserva(id) ON DELETE CASCADE,
  nombre TEXT NOT NULL,
  dni TEXT NOT NULL,
  edad INTEGER NOT NULL,
  talla TEXT,
  UNIQUE (reserva_id, dni)
);
"""

SEED_ACTIVIDADES = """
INSERT INTO actividad (id, nombre, requiere_talla, cupos_maximos, edad_minima)
VALUES
  (1, 'Tirolesa', 1, 10, 8),
  (2, 'Safari', 0, 8, NULL),
  (3, 'Palestra', 1, 12, 12),
  (4, 'Jardinería', 0, 12, NULL);
"""

SEED_TURNOS = """
INSERT INTO turno (id, actividad_id, inicio, fin, estado, cupos_disponibles, fecha)
VALUES
  (1, 1, '09:00', '09:30', 'abierto', 10, '2025-10-20'),
  (2, 1, '09:30', '10:00', 'abierto', 0, '2025-10-20'),
  (3, 2, '10:00', '10:30', 'abierto', 8, '2025-10-20'),
  (4, 4, '11:00', '11:30', 'abierto', 12, '2025-10-20'),
  (7, 3, '12:00', '12:30', 'abierto', 12, '2025-10-20');
"""

# --- Fixture principal ---
@pytest.fixture(scope="function")
def db_session():
    """
    Crea una base SQLite temporal, ejecuta DDL y seed, y devuelve una sesión aislada.
    """
    # Crear estructura y seed
    with engine.begin() as conn:
        for stmt in DDL_SCRIPT.split(";"):
            if stmt.strip():
                conn.execute(text(stmt))
        conn.execute(text(SEED_ACTIVIDADES))
        conn.execute(text(SEED_TURNOS))

    # Crear sesión temporal
    session = Session(bind=engine, future=True)

    try:
        yield session  # se pasa a los tests
    finally:
        # Rollback + limpieza total después de cada test
        session.rollback()
        session.close()
        with engine.begin() as conn:
            for stmt in ["DELETE FROM reserva_participante;",
                         "DELETE FROM reserva;",
                         "DELETE FROM turno;",
                         "DELETE FROM actividad;"]:
                conn.execute(text(stmt))
