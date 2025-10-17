from database.db import sesion
from datetime import datetime
from database.schemas import Reserva
import json


def inscribirse_a_actividad (id_turno, cantidad, tyc, participantes):
    with sesion as db:
        reserva = {
            "turno_id": id_turno,
            "cantidad_personas": cantidad,
            "estado": "pendiente",
            "tyc_aceptados": tyc,
            "creada_en": datetime.now().isoformat(),
            "participantes": str(participantes)  # Convertir la lista a string
        }
        nueva_reserva = Reserva(**reserva)
        db.add(nueva_reserva)
        db.commit()
        return {"status": "ok", "message": "Inscripción realizada con éxito", "datos_reserva": reserva}


        