from inscripcion_actividad import inscribirse_a_actividad

def test_inscripcion_basica_devuelve_respuesta_exitosa():
    id_turno = 1
    cantidad = 1
    tyc = 1
    participantes = [{"nombre": "Juan", "edad": 25, "talla_camisa": "M"}]
    respuesta = inscribirse_a_actividad(id_turno, cantidad, tyc, str(participantes))
    assert respuesta["status"] == "ok"


