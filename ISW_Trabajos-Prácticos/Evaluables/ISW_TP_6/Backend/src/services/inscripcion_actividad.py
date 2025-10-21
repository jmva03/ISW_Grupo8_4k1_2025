from database.db import sesion
from datetime import datetime
from database.schemas import Reserva, Turno, ReservaParticipante, Actividad
import json


def inscribirse_a_actividad(id_turno, cantidad, tyc, participantes):
    # Abrimos UNA sola sesión + transacción atómica
    with sesion as db, db.begin():
        # 0) Traer y BLOQUEAR el turno para evitar sobreventa
        turno = (
            db.query(Turno)
              .with_for_update()               # <-- bloqueo de fila
              .filter(Turno.id == id_turno)
              .first()
        )
        
        # Validacion de cupos disponibles
        validacion_cupos = validar_cupos_disponibles(id_turno, cantidad, db)
        if validacion_cupos["status"] != "ok":
            return validacion_cupos
        # Validacion de tyc aceptados
        validacion_tyc = validar_tyc_aceptados(tyc)
        if validacion_tyc["status"] != "ok":
            return validacion_tyc
        
        # Validacion de cantidad participantes
        validacion_cantidad = validar_cantidad_participantes(cantidad)
        if validacion_cantidad["status"] != "ok":
            return validacion_cantidad
        
        # Validacion de cantidad participantes igual a la cantidad
        validacion_participantes = validar_participantes_desigual_a_cantidad(cantidad, participantes)
        if validacion_participantes["status"] != "ok":
            return validacion_participantes
        # Importante: vestimenta se valida contra la ACTIVIDAD del turno
        actividad_id = getattr(turno, "actividad_id", None) or getattr(getattr(turno, "actividad", None), "id", None)
        validacion_vestimenta = validar_vestimenta_requerida(participantes, actividad_id, db)
        if validacion_vestimenta["status"] != "ok":
            return validacion_vestimenta

        # 2) Crear reserva
        reserva = {
            "turno_id": id_turno,
            "cantidad_personas": cantidad,
            "estado": "pendiente",
            "tyc_aceptados": int(tyc),
            "creada_en": datetime.now(),
        }
        nueva_reserva = Reserva(**reserva)
        db.add(nueva_reserva)
        db.flush()  # necesito nueva_reserva.id

        # 3) Insertar participantes
        for participante in participantes:
            data_paticipante = {
                "reserva_id": nueva_reserva.id,
                "nombre": participante.get("nombre"),
                "dni": participante.get("dni"),
                "edad": participante.get("edad"),
                "talla": participante.get("talla_vestimenta"),
            }
            db.add(ReservaParticipante(**data_paticipante))
        
        return {"status": "ok", "message": "Inscripción realizada con éxito", "datos_reserva": reserva}
    
def validar_vestimenta_requerida(participantes, id_actividad, db):
    if not id_actividad:
        return {"status": "ok"}
    actividad = db.query(Actividad).filter(Actividad.id == id_actividad).first()
    if actividad and actividad.requiere_talla:
        for p in participantes:
            if not p.get("talla_vestimenta"):
                return {"status": "Vestimenta requerida",
                        "message": "La actividad requiere especificar la talla de vestimenta para todos los participantes."}
    return {"status": "ok"}


def validar_cupos_disponibles(id_turno, cantidad, db):
    turno = db.query(Turno).filter(Turno.id == id_turno).first()
    if not turno:
        return {"status": "Turno no encontrado", "message": "El turno especificado no existe."}
    if (turno.cupos_disponibles or 0) >= cantidad:
        return {"status": "ok"}
    return {"status": "Sin cupos disponibles", "message": "No hay cupos suficientes para la cantidad solicitada."}

def validar_tyc_aceptados(tyc):
    if (tyc):
        return {"status": "ok"}
    return {"status": "No se aceptaron TYC", "message": "Debe aceptar los términos y condiciones para continuar con la inscripción."}

def validar_cantidad_participantes(cantidad):
    if cantidad > 0:
        return {"status": "ok"}
    else:
        return {"status": "Cantidad inválida", "message": "La cantidad de participantes debe ser mayor a cero."}
    
def validar_participantes_desigual_a_cantidad(cantidad, participantes):
    if cantidad == len(participantes):
        return {"status": "ok"}
    else:
        return {"status": "Cantidad inválida", "message": "La cantidad de participantes no coincide con la cantidad especificada."}
