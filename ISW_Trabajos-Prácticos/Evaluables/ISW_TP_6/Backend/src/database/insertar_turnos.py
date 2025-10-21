from datetime import date, datetime, time, timedelta
from sqlalchemy import create_engine, text
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent  # carpeta donde está este script
DB_PATH = BASE_DIR / "Actividad.db"
engine = create_engine(f"sqlite:///{DB_PATH}", echo=False)



# --- Generación de turnos (sin duplicar) ---
with engine.begin() as conn:
    # Traer actividades (id y cupos máximos)
    conn.execute(text("DELETE FROM turno"))
    conn.execute(text("Delete from reserva_participante;"))  # limpiar tu
    conn.execute(text("DELETE FROM sqlite_sequence WHERE name='turno';"))  
    conn.execute(text("Delete from reserva"))  #
                      
    actividades = conn.execute(
        text("SELECT id, cupos_maximos FROM actividad")
    ).fetchall()

    hoy = date.today()
    dias = 30  # rango: hoy + 30 días
    slot = timedelta(minutes=30)
    h_inicio = time(9, 0)
    h_fin = time(18, 0)  # último turno termina a las 18:00

    def es_feriado(d: date) -> bool:
        return (d.month, d.day) in [(12, 25), (1, 1)]

    for n in range(dias + 1):
        d = hoy + timedelta(days=n)
        if d.weekday() == 0 or es_feriado(d):  # 0 = lunes
            continue

        fecha_txt = d.strftime("%Y-%m-%d")
        dt = datetime.combine(d, h_inicio)
        fin_dia = datetime.combine(d, h_fin)

        while dt < fin_dia:
            dt_end = dt + slot
            ini_txt = dt.strftime("%H:%M")
            fin_txt = dt_end.strftime("%H:%M")

            for row in actividades:
                act_id, cupos = row.id, row.cupos_maximos

                # Evitar duplicados por (actividad, fecha, inicio, fin)
                ya_existe = conn.execute(
                    text("""
                        SELECT 1
                          FROM turno
                         WHERE actividad_id = :a
                           AND fecha = :f
                           AND inicio = :i
                           AND fin = :fn
                         LIMIT 1
                    """),
                    {"a": act_id, "f": fecha_txt, "i": ini_txt, "fn": fin_txt}
                ).fetchone()

                if not ya_existe:
                    conn.execute(
                        text("""
                            INSERT INTO turno (actividad_id, inicio, fin, estado, cupos_disponibles, fecha)
                            VALUES (:a, :i, :fn, 'abierto', :c, :f)
                        """),
                        {"a": act_id, "i": ini_txt, "fn": fin_txt, "c": cupos, "f": fecha_txt}
                    )

            dt = dt_end

print("✅ BD creada/sembrada y turnos generados (sin duplicar).")