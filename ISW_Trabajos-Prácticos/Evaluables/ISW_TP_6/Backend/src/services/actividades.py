# services/disponibilidad.py
from typing import List, Dict, Any, Optional
from database.db import sesion
from database.schemas import Actividad, Turno

def listar_disponibilidad(dia: str, actividad_id: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Devuelve las actividades que tienen turnos disponibles para el día dado.
    Si se pasa un actividad_id, limita a esa actividad.
    """
    with sesion as db:
        q = (
            db.query(Actividad, Turno)
              .join(Turno, Turno.actividad_id == Actividad.id)
              .filter(Turno.fecha == dia)
              .filter(Turno.estado == "abierto")
              .filter(Turno.cupos_disponibles > 0)
        )
        if actividad_id is not None:
            q = q.filter(Actividad.id == actividad_id)

        q = q.order_by(Actividad.nombre.asc(), Turno.inicio.asc())
        rows = q.all()

        # Agrupar actividades -> turnos
        actividades: Dict[int, Dict[str, Any]] = {}
        for a, t in rows:
            if a.id not in actividades:
                actividades[a.id] = {
                    "actividad_id": a.id,
                    "actividad": a.nombre,
                    "requiere_talla": a.requiere_talla,
                    "edad_minima": a.edad_minima,
                    "turnos": [],
                }
            actividades[a.id]["turnos"].append({
                "id": t.id,
                "inicio": t.inicio,
                "fin": t.fin,
                "cupos_disponibles": t.cupos_disponibles,
            })

        return list(actividades.values())