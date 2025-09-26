# Credit Cards App

Este servicio está encargado de procesar las ofertas. Incluye funciones para crear, obtener y borrar ofertas.

## Índice

- [Credit Cards App](#credit-cards-app)
  - [Índice](#índice)
  - [Estructura](#estructura)
  - [Ejecución](#ejecución)
    - [Versiones](#versiones)
  - [Variables de entorno](#variables-de-entorno)
    - [Comandos](#comandos)
  - [API Endpoints](#api-endpoints)
  - [Pruebas](#pruebas)
    - [Unitarias](#unitarias)
    - [Integración](#integración)
  - [Documentación técnica](#documentación-técnica)
  - [Autor](#autor)

## Estructura
```
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
    ├── adapters # Pruebas de los adaptadores
    │
    ├── api # Pruebas con Postman
    │
    ├── integration # Pruebas de integración usando Pytest
    │
    └── logic # Pruebas a las funciones de lógica
```
## Ejecución
### Versiones
**Python:** 3.12.9

**Poetry:** 2.1.4

## Variables de entorno
Para la conexión con la BD, cree un archivo `.env` donde declare la URL a la BD.
```env
DATABASE_URL=postgresql+psycopg2://{{user}}:{{password}}@{{host_name}}:5432/{{db_name}}

```

### Comandos
Instalar dependencias:
```bash
poetry install
```

Correr aplicación:
```bash
poetry run uvicorn src.main:app --host 0.0.0.0 --port 9000
```

## API Endpoints

- `POST /offers` - Crea una oferta
- `GET /offers/{offer_id}` - Trae una oferta en específico
- `GET /offers` - Trae todas las ofertas
- `DELETE /offers/{offer_id}` - Borra una oferta

Accede a la documentación después de ejecutar la aplicación:
- Swagger UI: `http://localhost:9000/docs`

## Pruebas

En el proyecto existen dos tipos de pruebas: unitarias y de integración.

### Unitarias
Las pruebas unitarias se componen de logic y adapters, aunque también se corren las pruebas dentro de integration dado que se usa pytest para esto.

Para correr las pruebas instale las dependencias y corra el siguiente comando:
```bash
poetry run pytest --cov=src -v -s --cov-fail-under=70 --cov-report term-missing
```

### Integración
Para correr las pruebas de integración (pruebas de Postman) debe tener instalado newman y el ambiente debe estar en ejecución.
```bash
npm i -g newman
```
Luego puede correr las pruebas de la siguiente forma:
```bash
newman run tests/api/offers_collection.json
```
> [!IMPORTANT]
> The environment uses as default the url http://localhost:3001. If the app is running in a different port or url you can change this by passing the environment variable:
> ```bash
> newman run tests/api/offers_collection.json --env-var "OFFERS_PATH={{url}}"
> ```

## Documentación técnica

La documentación de la arquitectura del sistema puede encontrarla en ____

## Autor

- Andrés Donoso - af.donoso@uniandes.edu.co
