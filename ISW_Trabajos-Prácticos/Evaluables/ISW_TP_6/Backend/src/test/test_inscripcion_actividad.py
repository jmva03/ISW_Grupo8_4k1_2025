from services.inscripcion_actividad import inscribirse_a_actividad

def test_inscripcion_basica_devuelve_respuesta_exitosa():
    id_turno = 1
    cantidad = 1
    tyc = 1
    participantes = [{"nombre": "Juan", "edad": 25, "talla_vestimenta": "M", "dni": "12345678"}]
    respuesta = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    assert respuesta["status"] == "ok"

def test_inscripcion_sin_vestimenta_requerida():
    id_turno = 7
    cantidad = 2
    tyc = 1
    participantes = [{"nombre": "Juan","dni": "4568786", "edad": 25, "talla_vestimenta": "S"}, {'nombre': 'Pedro', 'dni': '12345678', 'edad': 30}]
    respuesta = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    assert respuesta["status"] == "Vestimenta requerida"

def test_inscripcion_sin_vestimenta_no_requerida():
    id_turno = 4
    cantidad = 1
    tyc = 1
    participantes = [{"nombre": "Luis", "dni": "98765432", "edad": 28}]
    respuesta = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    assert respuesta["status"] == "ok"

def test_inscripcion_actividad_sin_cupos():
    id_turno = 2  # Asumiendo que el turno con ID 2 no tiene cupos disponibles
    cantidad = 1
    tyc = 1
    participantes = [{"nombre": "Ana", "dni": "12345678", "edad": 30, "talla_vestimenta": "L"}]
    respuesta = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    assert respuesta["status"] == "Sin cupos disponibles"
def test_inscripcion_sin_tyc_aceptados():
    id_turno = 1
    cantidad = 1
    tyc = 0  # Términos y condiciones no aceptados
    participantes = [{"nombre": "Marta", "dni": "87654321", "edad": 22, "talla_vestimenta": "S"}]
    respuesta = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    assert respuesta["status"] == "No se aceptaron TYC"

def test_inscripcion_sin_cantidad_participantes():
    id_turno = 1
    cantidad = 0
    tyc = 1
    participantes = []
    respuesta = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    assert respuesta["status"] == "Cantidad inválida"
