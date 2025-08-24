# Routes app

Esta app está desarrollada en FastAPI que implementa una arquitectura hexagonal modificada para gestionar la entidad Routes. La aplicación se ejecuta haciendo uso de docker y puede ser ejecutada directamente haciendo uso de k8s.

## Índice

- [Routes app](#routes-app)
  - [Índice](#índice)
  - [Estructura](#estructura)
  - [Ejecución](#ejecución)
    - [Versiones](#versiones)
  - [Variables de entorno](#variables-de-entorno)
    - [Comandos](#comandos)
      - [Instalar dependencias y correr app](#instalar-dependencias-y-correr-app)
      - [Ejecutar en Docker](#ejecutar-en-docker)
      - [Ejecutar en Minikube](#ejecutar-en-minikube)
  - [API Endpoints](#api-endpoints)
  - [Pruebas](#pruebas)
    - [Unitarias](#unitarias)
    - [Integración](#integración)
  - [Autor](#autor)

## Estructura

```
.
├── src # Código de la aplicación
│   ├── adapters # Funciones para convertir entre objetos que entran y salen de la aplicación
│   │
│   ├── api # Lógica para comunicación con otros servicios usando http.
│   │   └── http_server.py # EPs expuestos por este servicio
│   │
│   ├── controllers # Lógica de negocio del servicio.
│   │
│   ├── database # Configuraciones de la base de datos
│   │
│   ├── exceptions # Excepciones personalizadas
│   │
│   ├── logic # Funciones puras que contienen lógica
│   │
│   ├── models # Modelos de la aplicación
│   │   ├── incoming # Modelos que entran a la app (e.g. body de una petición http)
│   │   │
│   │   ├── internal # Modelos internos de la app (mismos de la BD)
│   │   │
│   │   └── out # Modelos que salen de la app (e.g. body de una respuesta http)
│   │
│   ├── repositories # Establecen la comunicación con la BD
│   │
│   ├── assembly.py # Crea los controlodares e inyecta el repositorio
│   │
│   └── main.py # Punto de inicio de la aplicación
│
└── tests # Pruebas de la aplicación
    ├── api # Pruebas con Postman
    │
    └── unit # Pruebas unitarias usando Pytest
├── Dockerfile              # Configuración de Docker
├── docker-compose.yml      # Configuración de multicontenedores con Docker - para pruebas locales
├── pyproject.toml          # Configuración de Poetry
└── README.md               # Este archivo
```

## Ejecución
### Versiones
**Python:** 3.12.9

**Poetry:** 2.1.4

## Variables de entorno
Para la conexión con la BD, cree un archivo `.env` donde declare la URL a la BD.
```env
DATABASE_URL=postgresql://{{user}}:{{password}}@{{host_name}}:5432/{{db_name}}
```

### Comandos
#### Instalar dependencias y correr app

Instalar dependencias:
```bash
poetry install
```

Correr aplicación:
```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 9000
```

#### Ejecutar en Docker

```bash
APP_VERSION = routes-app
APP_NAME = 1.0.0
docker build --rm --platform linux/amd64 -t ${APP_NAME}:${APP_VERSION} -f Dockerfile --target runner --label version=${APP_VERSION} .

docker run --platform linux/amd64 -p 9000:9000 ${APP_NAME}:${APP_VERSION}
```

#### Ejecutar en Minikube

Después de haber creado la imagen haciendo uso de docker, ejecute:

```bash
minikube start --cpus=2 --memory=3g --cni calico

#make mkbuild
minikube image load ${APP_NAME}:${APP_VERSION}

kubectl apply -f .\k8s\routes-app-deployment.yaml
minikube service routes-app-service
```

Minikube asignará un puerto para que pueda acceder a su servicio. Puede usarlo en su browser o en postman.

## API Endpoints

- `POST /routes` - Crea un trayecto
- `GET /routes?flight={flightId}` - Ver y filtrar trayectos
- `GET /routes/{id}` - Consultar un trayecto
- `DELETE /routes/{id}` - Eliminar trayecto
- `GET /routes/count` - Consultar cantidad de entidades
- `GET /routes/ping` - Consulta de salud del servicio
- `POST /routes/reset` - Restablecer base de datos
  
Accede a la documentación después de ejecutar la aplicación:
- Swagger UI: `http://localhost:9000/docs`

## Pruebas

El proyecto contempla dos paquetes de pruebas: pruebas unitarias y pruebas de API (Integración).

### Unitarias

Se usó un [fixture](https://docs.pytest.org/en/stable/explanation/fixtures.html) para crear recursos reutilizables en las pruebas y de configuración. Estos fixtures están ubicados en el archivo `conftest.py`.

Para ejecutar las pruebas unitarias y establecer el porcentaje mínimo de cobertura del conjunto de pruebas en 70%, ejecuta el siguiente comando:

```bash
poetry install
poetry run pytest --cov=src -v -s --cov-fail-under=70 --cov-report term-missing
```

### Integración

Las pruebas de integración se realizan por medio de Postman y newman. Encontrará un archivo de colección de postman en la carpeta `tests/api/` el cuál puede cargar en su aplicación de postman de manera local. Posteriormente puede ejecutar `Run collection` para verificar que la aplicación está funcionando correctamente. Tener en cuenta de asignar la URL adecuada.

## Autor

- Germán Martínez - [gd.martinez@uniandes.edu.co](mailto:gd.martinez@uniandes.edu.co)