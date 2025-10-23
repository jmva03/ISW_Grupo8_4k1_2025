Guía de estilos para el Frontend.

Esta otra parte del segmento también va a estar dedicado a las convenciones que se tienen que tener en cuenta al momento de la implementación. Como se implementa en el mismo entorno de desarrollo que el backend, también se utilizara el “Visual studio code” con las extensiones necesaria para la detección de errores y formateo automático. 

No esta mal volver a explicar que utilizamos esta convención por lo que fuimos aprendiendo a lo largo de la carrera y porque nos sentimos comodos al trabajar de esta forma.


1. La Base: Guía Airbnb para JavaScript/React
Nos basamos en la popular Guía de Estilo de Airbnb para JavaScript. Es muy completa y nos ayuda a mantener el código ordenado y consistente. Se la puede ver en su pagina oficial en el siguiente link: https://airbnb.io/javascript/react/
2. Nombres Claros
Siguiendo las convenciones de Airbnb y React:
Componentes React y nombres de archivo de componentes: Usamos “PascalCase”.
Variables, funciones, props, y nombres de archivo no-componentes: Usamos “camelCase”`.
3. Comentarios y Documentación
Comentarios en línea: Usamos “//” para explicar la funcionalidad del código.
4. Estilo para Componentes React
Componentes Funcionales: Preferimos usar componentes funcionales con Hooks (“useState”, “useEffect”, etc.).
Props:
	•Desestructurar las props al inicio del componente para mayor claridad.
	•Definir los tipos de las props usando “propTypes”.
Estado: Usar “useState” para estados simples, “useReducer” para lógica de estado más compleja.
Efectos: Usar “useEffec”` con un array de dependencias claro y específico para evitar ejecuciones innecesarias.

JSX:
	•Mantener el JSX lo más limpio posible, extrayendo lógica compleja a funciones fuera del “return”.
	•Usar paréntesis “()” para JSX multilínea.
5. Importaciones, se utiliza las “Alias de Ruta con ‘@’ ”: Para evitar rutas relativas largas y confusas, utilizamos el alias “@” que apunta directamente a la carpeta “src” para de esa forma realizar importaciones. 
	•Debemos usar: “import { Boton } from '@/components/ui/Boton';” 
	•Evitar: “import { Boton } from '../../../components/ui/Boton';” 
	•Orden: Aunque ESLint suele ordenarlo automáticamente, intentamos agrupar los imports: primero los de React, luego librerías externas, y finalmente nuestros propios módulos usando 	el alias “@”.
