# Sushi Bunny

Sushi Bunny es una aplicación desarrollada como parte de una serie de proyectos que deben completarse en menos de 2 horas. La aplicación permite gestionar mesas en las que cada integrante puede registrar cuántas piezas de sushi ha comido. Además, ofrece un resumen de la actividad de cada mesa.

## Funcionalidades principales
- Crear una mesa para los integrantes.
- Registrar el consumo de sushi por cada integrante.
- Visualizar un resumen del consumo de sushi por mesa.

## Endpoints

### `/`
La página principal de la aplicación. Permite crear una nueva mesa.

### `/mesa/<mesa_id>`
La sala de una mesa específica. Aquí puedes seleccionar tu nombre y registrar cuántas piezas de sushi estás comiendo.

### `/mesas`
Muestra una lista de todas las mesas creadas.

### `/resume/<mesa_id>`
Proporciona un resumen detallado del consumo de sushi en una mesa específica.

## Tecnologías utilizadas

Este proyecto ha sido desarrollado utilizando las siguientes tecnologías:
- **FastAPI**: Para la creación de la API y manejo de endpoints.
- **Websockets**: Para la comunicación en tiempo real entre los usuarios.
- **Jinja2**: Para la renderización de plantillas HTML.
- **PostgreSQL**: Como base de datos para almacenar la información de las mesas y el consumo de sushi.