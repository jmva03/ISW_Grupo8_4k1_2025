from typing import List, Optional, Literal, Annotated
from pydantic import BaseModel, Field

# --------- Request ---------
class ParticipanteIn(BaseModel):
    nombre: Optional[str] = None
    dni: Optional[str] = None      # <- permitir None o string vacío
    edad: Optional[int] = None
    talla_vestimenta: Optional[str] = None

# Enteros > 0 usando Annotated + Field
PosInt = Annotated[int, Field(gt=0)]
# 0 o 1
ZeroOne = Annotated[int, Field(ge=0, le=1)]

class InscripcionIn(BaseModel):
    id_turno: int
    cantidad: int
    tyc: int
    participantes: List[ParticipanteIn]

class DatosReservaOut(BaseModel):
    turno_id: int
    cantidad_personas: int
    estado: str
    tyc_aceptados: int
    creada_en: Optional[str] | None = None  

class InscripcionOut(BaseModel):
    status: Literal[
        "ok",
        "Turno no encontrado",
        "Sin cupos disponibles",
        "No se aceptaron TYC",
        "Cantidad inválida",
        "Vestimenta requerida",
    ]
    message: str
    datos_reserva: Optional[DatosReservaOut] = None

class TurnoSlotOut(BaseModel):
    id: int
    inicio: str
    fin: str
    cupos_disponibles: int

class ActividadDisponibilidadOut(BaseModel):
    actividad_id: int
    actividad: str
    requiere_talla: int
    edad_minima: Optional[int] = None
    turnos: List[TurnoSlotOut]
