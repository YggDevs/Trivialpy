# Trivialpy
Trivial de preguntas utilizando sockets
# Servidor de Juego de Preguntas y Respuestas

Este proyecto implementa un servidor de juego de preguntas y respuestas multijugador utilizando Python y sockets.

## Características

- Soporte para múltiples jugadores simultáneos
- Carga de preguntas desde un archivo JSON
- Sistema de turnos con límite de tiempo
- Puntuación y ranking de jugadores
- Manejo de reconexiones de jugadores

## Requisitos

- Python 3.7+
- Módulos de Python: `socket`, `json`, `random`, `threading`, `time`, `logging`

## Instalación

1. Clona este repositorio:

git clone https://github.com/tu-usuario/nombre-del-repo.git
2. Navega al directorio del proyecto:
Claro, aquí tienes un ejemplo de un archivo README.md para tu proyecto de servidor de juegos de preguntas y respuestas:

```markdown
# Servidor de Juego de Preguntas y Respuestas

Este proyecto implementa un servidor de juego de preguntas y respuestas multijugador utilizando Python y sockets.

## Características

- Soporte para múltiples jugadores simultáneos
- Carga de preguntas desde un archivo JSON
- Sistema de turnos con límite de tiempo
- Puntuación y ranking de jugadores
- Manejo de reconexiones de jugadores

## Requisitos

- Python 3.7+
- Módulos de Python: `socket`, `json`, `random`, `threading`, `time`, `logging`

## Instalación

1. Clona este repositorio:
   ```
   git clone https://github.com/tu-usuario/nombre-del-repo.git
   ```
2. Navega al directorio del proyecto:
   ```
   cd nombre-del-repo
   ```

## Uso

### Servidor

1. Ejecuta el servidor:
   ```
   python server.py
   ```
2. El servidor comenzará a escuchar conexiones en el puerto 65432 (por defecto).

### Cliente

1. Ejecuta el cliente:
   ```
   python client.py
   ```
2. Sigue las instrucciones en pantalla para unirte al juego.

## Configuración

- El archivo de preguntas debe estar en formato JSON. Puedes especificar la ruta del archivo al iniciar el servidor o se te pedirá que lo selecciones.
- Puedes modificar el puerto del servidor y otros parámetros en el archivo `server.py`.

## Estructura del Proyecto

- `server.py`: Contiene la lógica del servidor del juego.
- `client.py`: Implementa el cliente para conectarse al servidor.
- `preguntas.json`: Archivo de ejemplo con las preguntas del juego.

## Contribuir

Las contribuciones son bienvenidas. Por favor, abre un issue para discutir cambios mayores antes de hacer un pull request.

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

yggdev 


```

