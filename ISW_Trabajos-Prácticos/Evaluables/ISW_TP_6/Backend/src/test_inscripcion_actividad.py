from inscripcion_actividad import inscribirse_a_actividad

def test_inscripcion_basica_devuelve_respuesta_exitosa():
    respuesta = inscribirse_a_actividad()
    assert respuesta == 1