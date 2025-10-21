from fastapi import APIRouter, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from typing import List, Optional
from dtos.models import InscripcionIn, InscripcionOut, ActividadDisponibilidadOut
from services.actividades import listar_disponibilidad
from services.inscripcion_actividad import inscribirse_a_actividad

router = APIRouter()


@router.post("/inscripciones", response_model=InscripcionOut, status_code=status.HTTP_201_CREATED)
def crear_inscripcion(payload: InscripcionIn):
     pass

@router.get("/disponibilidad", response_model=List[ActividadDisponibilidadOut])
def get_disponibilidad():
     pass