from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine('sqlite:///Actividad.db')

ddl = """
CREATE TABLE IF NOT EXISTS actividad (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  nombre TEXT NOT NULL UNIQUE,
  requiere_talla INTEGER NOT NULL DEFAULT 0,  -- 0 = False, 1 = True
  cupos_maximos INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS turno (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  actividad_id INTEGER NOT NULL REFERENCES actividad(id),
  inicio TEXT NOT NULL,
  fin TEXT NOT NULL,
  estado TEXT NOT NULL DEFAULT 'abierto',
  cupos_disponibles INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS reserva (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  turno_id INTEGER NOT NULL REFERENCES turno(id),
  cantidad_personas INTEGER NOT NULL,
  estado TEXT NOT NULL DEFAULT 'pendiente',
  tyc_aceptados INTEGER NOT NULL DEFAULT 0,  -- 0 = False, 1 = True
  creada_en TEXT NOT NULL,
  participantes TEXT NOT NULL  -- guardás JSON como string
);
"""

ddl_insertar_datos = """
-- Agregar edad_minima a ACTIVIDAD
ALTER TABLE actividad ADD COLUMN edad_minima INTEGER;

-- Marcar requiere_talla y setear cupos/edad mínima
INSERT INTO actividad (nombre, requiere_talla, cupos_maximos, edad_minima) VALUES
  ('Tirolesa',   1, 10, 8),
  ('Safari',     0,  8, NULL),
  ('Palestra',   1, 12, 12),
  ('Jardinería', 0, 12, NULL);

-- Agregar columna fecha a TURNO
ALTER TABLE turno ADD COLUMN fecha TEXT NOT NULL DEFAULT '';
"""
with engine.begin() as connection:
    for stmt in ddl_insertar_datos.split(";"):
        if stmt.strip():
            connection.execute(text(stmt))
