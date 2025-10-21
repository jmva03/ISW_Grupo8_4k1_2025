from datetime import date, datetime, time, timedelta
from pathlib import Path

from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import Session

# --- paths/engine/sesión ---
BASE_DIR = Path(__file__).resolve().parent  # carpeta donde está este script
DB_PATH = BASE_DIR / "Actividad.db"
engine = create_engine(
    f"sqlite:///{DB_PATH}",
    echo=False,
    future=True,
)

# Habilitar FKs en SQLite
@event.listens_for(engine, "connect")
def _enable_sqlite_fk(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()

sesion = Session(bind=engine, future=True)

# --- DDL (creación limpia) ---
ddl = """
CREATE TABLE IF NOT EXISTS actividad (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL UNIQUE,
  requiere_talla INTEGER NOT NULL DEFAULT 0,  -- 0 = False, 1 = True
  cupos_maximos INTEGER NOT NULL,
  edad_minima INTEGER
);

CREATE TABLE IF NOT EXISTS turno (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  actividad_id INTEGER NOT NULL REFERENCES actividad(id),
  inicio TEXT NOT NULL,                         -- HH:MM
  fin    TEXT NOT NULL,                         -- HH:MM
  estado TEXT NOT NULL DEFAULT 'abierto',
  cupos_disponibles INTEGER NOT NULL,
  fecha  TEXT NOT NULL DEFAULT ''               -- YYYY-MM-DD
);

CREATE TABLE IF NOT EXISTS reserva (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  turno_id INTEGER NOT NULL REFERENCES turno(id),
  cantidad_personas INTEGER NOT NULL,
  estado TEXT NOT NULL DEFAULT 'pendiente',
  tyc_aceptados INTEGER NOT NULL DEFAULT 0,     -- 0 = False, 1 = True
  creada_en DATETIME NOT NULL                   -- ahora DateTime
);

CREATE TABLE IF NOT EXISTS reserva_participante (
  id           INTEGER PRIMARY KEY AUTOINCREMENT,
  reserva_id   INTEGER NOT NULL REFERENCES reserva(id) ON DELETE CASCADE,
  nombre       TEXT NOT NULL,
  dni          TEXT NOT NULL,
  edad         INTEGER NOT NULL,
  talla        TEXT,                            -- NULL si la actividad no requiere
  UNIQUE (reserva_id, dni)                      -- evita duplicar una misma persona en la misma reserva
);
"""

# --- Seed base (actividades + ajustes iniciales) ---
seed_actividades = """
INSERT OR IGNORE INTO actividad (id, nombre, requiere_talla, cupos_maximos, edad_minima) VALUES
  (1, 'Tirolesa',   1, 10, 8),
  (2, 'Safari',     0,  8, NULL),
  (3, 'Palestra',   1, 12, 12),
  (4, 'Jardinería', 0, 12, NULL);
"""

# (Opcional) ejemplo para marcar sin cupos el turno id=2 si existiera
reiniciar_bd = """
Delete from turno;
Delete from reserva_participante;
DELETE FROM sqlite_sequence WHERE name='turno';
Delete from reserva;;
"""
ddl_consultas = """
UPDATE turno
   set cupos_disponibles = 0
    where id = 2;
"""

# --- Ejecutar DDL/Seed ---
with engine.begin() as connection:
    for stmt in ddl_consultas.split(";"):
        if stmt.strip():
            connection.execute(text(stmt))

    # Seed de actividades
    connection.execute(text(seed_actividades))