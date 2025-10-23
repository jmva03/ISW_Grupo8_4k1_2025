# ISW_Grupo8_4k1_2025
Estilo del código para el Backend

Este segmento va a estar dedicado para que todos los del grupo estemos de acuerdo sobre cual estándar se va a seguir para escribir el código del backend. La idea es que sea fácil de leer, entender y modificar por cualquiera de nosotros. Elegimos estas convención, porque fueron los estilos de código que fuimos aprendiendo a lo largo de la carrera y por tanto nos sentimos comodos con el uso del mismo.

1- La Base: PEP 8

Vamos a seguir principalmente la guía ""PEP 8"", que es como el "manual de estilo" estándar de Python. No es necesario que la aprendamos de memoria, pero si que la tengamos en cuenta al momento de la implementación.

Se puede consultar la guía completa en este link: https://peps.python.org/pep-0008/ 

2. Nuestro Entorno de desarrollo va a ser el Visual Studio Code para asegurarnos que todos escribamos código con el mismo estilo y detectar errores comunes. Se va a también implementar las extensiones de formateo automático y detección de errores.

3. Nomenclatura acorde a las convenciones de Python (PEP 8):

Variables y funciones: Usamos snake_case (todo en minúscula, separando palabras con guion bajo). Ej: contador_usuarios.
Clases: Usamos “CamelCase” (empezando cada palabra con mayúscula). 

4. Los comentarios dentro del código (#) son para explicar que hace una funcionalidad. 

5. Estilo para Endpoints de API (FastAPI) Como usamos FastAPI para crear nuestras APIs, seguimos estas pautas:  
	•Nombres de Rutas (Paths):  Usar sustantivos en plural para referirse a colecciones de recursos (ej: /inscripciones). 
	•Usar identificadores de ruta para recursos específicos.
	•Todo en minúsculas y separando palabras con guion medio (-) si es necesario (aunque preferimos rutas simples). 
	•Métodos HTTP:  
		o GET: Para obtener datos (listar colecciones o un recurso específico).
		o POST: Para crear nuevos recursos.  
		o PUT: Para actualizar completamente un recurso existente.  
		o DELETE: Para eliminar un recurso.
6. Estilo para pruebas (pytest)
Para asegurarnos de que el código funciona como esperamos, usamos pytest. Nuestras convenciones son:
	• Nombres de Archivos: Los archivos de prueba deben empezar con test.
	• Nombres de Funciones: Las funciones de prueba deben empezar con test_ (ej: test_iistar_disponibilidad_sin_filtros():).
	• Estructura (Arrange-Act-Assert): Intentamos seguir este patrón:
		1.Arrange: Preparar los datos y el estado necesario para la prueba.
		2.Act: Ejecutar la función o método que queremos probar.
		3.Assert: Verificar que el resultado es el esperado usando assert.
