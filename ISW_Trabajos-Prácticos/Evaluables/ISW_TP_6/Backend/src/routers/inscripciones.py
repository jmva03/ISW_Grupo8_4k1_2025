from fastapi import APIRouter, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from dtos.models import InscripcionIn, InscripcionOut, ActividadDisponibilidadOut
from services.actividades import listar_disponibilidad
from services.inscripcion_actividad import inscribirse_a_actividad

router = APIRouter()


@router.post("/inscripciones", response_model=InscripcionOut, status_code=status.HTTP_201_CREATED)
def crear_inscripcion(payload: InscripcionIn):
    # Llamamos a tu servicio tal cual
    r = inscribirse_a_actividad(
        id_turno=payload.id_turno,
        cantidad=payload.cantidad,
        tyc=payload.tyc,
        participantes=[p.model_dump() for p in payload.participantes],
    )

    s = r.get("status", "Cantidad inválida")

    # Normalizamos la serialización (datetime -> ISO) solo al devolver
    if "datos_reserva" in r and r["datos_reserva"] is not None:
        r = jsonable_encoder(r)  # convierte datetime a str ISO para JSON

    if s == "ok":
        return r

    if s == "Turno no encontrado":
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=r)

    if s == "Sin cupos disponibles":
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=r)

    if s in ["Faltan datos", "error", "Vestimenta requerida", "Edad mínima no cumplida"]: 
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=r)
    

@router.get("/disponibilidad", response_model=List[ActividadDisponibilidadOut])
def get_disponibilidad(
    dia: str = Query(..., description="Día a consultar (YYYY-MM-DD)"),
    actividad_id: Optional[int] = Query(None, description="Filtra por actividad específica"),
):
    """
    Devuelve actividades con sus turnos disponibles para el día dado.
    Si se pasa 'actividad_id', limita la respuesta a esa actividad.
    """
    return listar_disponibilidad(dia=dia, actividad_id=actividad_id)
