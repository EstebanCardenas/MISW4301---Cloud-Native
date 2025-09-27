# Notifications App

Este servicio está encargado de enviar notificaciones

## Índice

- [notifications App](#notifications-app)
  - [Índice](#índice)
  - [Estructura](#estructura)
  - [Ejecución](#ejecución)
    - [Versiones](#versiones)
  - [API Endpoints](#api-endpoints)
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
    │
    ├── assembly.py # Crea los controlodares e inyecta el repositorio
    │
    └── main.py # Punto de inicio de la aplicación
```
## Ejecución
### Versiones
**Python:** 3.12.9

**Poetry:** 2.1.4

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

`POST /notifications/posts/`
```
Body

{
    // rf-006 | rf-007
    "template": "XXXX",
    
    // email destinatario
    "to": "xxxx@xxx.xxx",

    // Asunto del mail
    "subject": "xxxxxx",

    // llave-valor para reemplazar cosas en el template
    "data": {
        "key1": "abc-123",
        "key2": "xyz-987",
        "keyn": "123"
    }
}

```

Accede a la documentación después de ejecutar la aplicación:
- Swagger UI: `http://localhost:9000/docs`

## Autor

- Daniel Corzo - d.corzos@uniandes.edu.co
