export interface DataResponse {
  actividad_id: number
  actividad: string
  requiere_talla: number
  edad_minima: null
  turnos: Turno[]
}

export interface Turno {
  id: number
  inicio: string
  fin: string
  cupos_disponibles: number
}

export interface ParticipantDetails {
  fullName: string
  dni: string
  age: string
  clothingSize?: string
}