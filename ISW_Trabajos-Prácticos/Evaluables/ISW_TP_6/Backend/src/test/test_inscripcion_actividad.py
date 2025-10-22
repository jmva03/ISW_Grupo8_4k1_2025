
from services.inscripcion_actividad import inscribirse_a_actividad
from services. actividades import listar_disponibilidad
from database.db import sesion
from fastapi.testclient import TestClient
from src.main import app


import sys
print("PYTHONPATH:\n", "\n".join(sys.path[:5]))
def test_inscripcion_basica_devuelve_respuesta_exitosa():
    id_turno = 1
    cantidad = 1
    tyc = 1
    participantes = [{"nombre": "Eugenio", "dni": "4568786", "edad": 25, "talla_vestimenta": "M"}]
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

def test_inscripcion_participantes_desigual_a_cantidad():
    id_turno = 7
    cantidad = 3
    tyc = 1
    participantes = [{"nombre": "Carlos", "dni": "11223344", "edad": 29, "talla_vestimenta": "M"}]  # Solo un participante en la lista
    respuesta = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    assert respuesta["status"] == "Cantidad inválida"

def test_validar_participante_estructura_ok():
    id_turno = 1
    cantidad = 2
    tyc = 1
    participantes = [
        {"nombre": "Ana", "dni": "1232342", "edad": 20, "talla_vestimenta": "S"},
        {"nombre": "Luis", "dni": "4563432", "edad": 35, "talla_vestimenta": "L"}
    ]
    r = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    assert r["status"] == "ok"

def test_validar_participante_estructura_faltan_datos():
    id_turno = 1
    cantidad = 1
    tyc = 1
    participantes = [
        {"nombre": "Ana", "dni": "", "edad": 20, "talla_vestimenta": "S"}, 
    ]
    r = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    assert r["status"] == "Faltan datos"
    assert "Faltan datos" in r["message"]

def test_validar_participante_estructura_sin_edad():
    id_turno = 1
    cantidad = 1
    tyc = 1
    participantes = [
        {"nombre": "Ana", "dni": "123", "talla_vestimenta": "M"}  # falta edad
    ]
    r = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    assert r["status"] == "Faltan datos"

def test_listar_disponibilidad_sin_filtros():
    dia = "2024-12-01"
    disponibilidad = listar_disponibilidad(dia=dia)
    assert isinstance(disponibilidad, list)
    for actividad in disponibilidad:
        assert "actividad_id" in actividad
        assert "actividad" in actividad
        assert "turnos" in actividad
        for turno in actividad["turnos"]:
            assert "id" in turno
            assert "inicio" in turno
            assert "fin" in turno
            assert "cupos_disponibles" in turno

def test_listar_disponibilidad_con_filtro_actividad():
    dia = "2024-12-01"
    actividad_id = 1  # Suponiendo que existe una actividad con ID 1
    disponibilidad = listar_disponibilidad(dia=dia, actividad_id=actividad_id)
    assert isinstance(disponibilidad, list)
    for actividad in disponibilidad:
        assert actividad["actividad_id"] == actividad_id
        for turno in actividad["turnos"]:
            assert "id" in turno
            assert "inicio" in turno
            assert "fin" in turno
            assert "cupos_disponibles" in turno

def test_api_inscripcion_crear_inscripcion():

    client = TestClient(app)

    payload = {
        "id_turno": 1,
        "cantidad": 1,
        "tyc": 1,
        "participantes": [
            {"nombre": "Sofia", "dni": "99887766", "edad": 27, "talla_vestimenta": "M"}
        ]
    }

    response = client.post("/inscripciones", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "ok"
    assert "datos_reserva" in data

def test_api_disponibilidad_get_disponibilidad():

    client = TestClient(app)

    dia = "2024-12-01"
    response = client.get(f"/disponibilidad?dia={dia}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for actividad in data:
        assert "actividad_id" in actividad
        assert "actividad" in actividad
        assert "turnos" in actividad

def test_inscripcion_falla_por_formato_dni_o_nombre():
    id_turno = 1
    cantidad = 1
    tyc = 1

    # --- Caso 1: DNI con letras (debe fallar) ---
    participantes_dni_letras = [{"nombre": "Alice", "dni": "1234567A", "edad": 25, "talla_vestimenta": "M"}]
    respuesta_dni_letras = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes_dni_letras)
    assert respuesta_dni_letras["status"] == "error"
    assert "solo números" in respuesta_dni_letras["message"]

    # --- Caso 2: DNI con longitud incorrecta (6 dígitos, debe fallar) ---
    participantes_dni_corto = [{"nombre": "Bob", "dni": "123456", "edad": 30, "talla_vestimenta": "L"}]
    respuesta_dni_corto = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes_dni_corto)
    assert respuesta_dni_corto["status"] == "error"
    assert "entre 7 y 8 dígitos" in respuesta_dni_corto["message"]

    # --- Caso 3: Nombre con números (debe fallar) ---
    participantes_nombre_numeros = [{"nombre": "Cloe123", "dni": "88776655", "edad": 22, "talla_vestimenta": "S"}]
    respuesta_nombre_numeros = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes_nombre_numeros)
    assert respuesta_nombre_numeros["status"] == "error"
    assert "no puede contener números" in respuesta_nombre_numeros["message"]

    # --- Caso 4: Nombre muy corto (1 caracter, debe fallar) ---
    participantes_nombre_corto = [{"nombre": "D", "dni": "12345678", "edad": 40, "talla_vestimenta": "XL"}]
    respuesta_nombre_corto = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes_nombre_corto)
    assert respuesta_nombre_corto["status"] == "error"

def test_inscripcion_falla_por_edad_minima_no_cumplida():
    id_turno = 5
    cantidad = 2
    tyc = 1
    
    participantes = [
        {"nombre": "Adulto OK", "dni": "11223344", "edad": 0, "talla_vestimenta": "M"}, 
        {"nombre": "Menor No OK", "dni": "55667788", "edad": 15, "talla_vestimenta": "S"}
    ]
    
    respuesta = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    
    assert respuesta["status"] == "Edad mínima no cumplida"
    assert "no cumple con la edad mínima requerida" in respuesta["message"]

def test_inscripcion_exitosa_si_cumplen_edad_minima():
    id_turno = 4 
    cantidad = 1
    tyc = 1
    
    participantes = [
        {"nombre": "Juan Adulto", "dni": "99001122", "edad": 20, "talla_vestimenta": "L"}
    ]
    
    respuesta = inscribirse_a_actividad(id_turno, cantidad, tyc, participantes)
    
    assert respuesta["status"] == "ok"
