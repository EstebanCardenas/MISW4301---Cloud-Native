# Users API

Aplicación para gestión de usuarios desarrollada con Go utilizando Gin como web framework y GORM como ORM.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
6. [Autor](#autor)

## Estructura

```
.
├── Dockerfile
├── README.md
├── cmd
│   └── http
│       └── main.go # Punto de entrada de la app
├── docker-compose.yml
├── go.mod
├── go.sum
├── internal # Implementaciones internas del módulo
│   ├── adapter
│   │   ├── auth # Servicio de token
│   │   │   ├── mock
│   │   │   │   └── token.go
│   │   │   └── token.go
│   │   ├── data # Capa de datos (SQL/GORM)
│   │   │   ├── mock
│   │   │   │   ├── repository
│   │   │   │   │   └── user.go
│   │   │   │   └── test_db.go
│   │   │   └── postgres
│   │   │       ├── db.go
│   │   │       ├── models # Entidades de BD
│   │   │       │   └── user.go
│   │   │       └── repository
│   │   │           ├── user.go
│   │   │           └── user_test.go
│   │   ├── handler # Handlers HTTP
│   │   │   └── http
│   │   │       ├── auth.go
│   │   │       ├── auth_test.go
│   │   │       ├── error.go
│   │   │       ├── middleware.go
│   │   │       ├── middleware_test.go
│   │   │       ├── response.go
│   │   │       ├── router.go
│   │   │       ├── user.go
│   │   │       └── user_test.go
│   │   └── hash # Servicio para hashing de contraseñas
│   │       ├── bycrypt.go
│   │       └── mock
│   │           └── hash.go
│   └── core
│       ├── domain # Modelos de dominio
│       │   ├── error.go
│       │   └── user.go
│       ├── port # Definiciones de interfaces
│       │   ├── auth.go
│       │   ├── hash.go
│       │   ├── token.go
│       │   └── user.go
│       └── service # Capa de lógica de negocio
│           ├── auth.go
│           ├── auth_test.go
│           ├── mock
│           │   ├── auth.go
│           │   └── user.go
│           ├── user.go
│           └── user_test.go
└── scripts
    └── test.sh
```

## Ejecución

1. Instalar Docker
2. Ingresar a la carpeta users (`cd users`)
3. Copiar los contenidos de `.env.example` en `.env`
4. Ejecutar `docker compose up -d`
5. La aplicación estará disponible en `http://0.0.0.0:8080`

## Uso

**URL base por defecto:** `http://localhost:8080`

- `POST /users/reset` - Resetea la BD
- `POST /users` - Crea un usuario
- `PATCH /users/:id` - Actualiza un usuario a partir del uuid
- `POST /users/auth` - Genera un token a partir de las credenciales
- `GET /users/me` - Consulta la información del usuario a partir del token
- `GET /users/count` - Consulta la cantidad de usuarios en el sistema
- `GET /users/ping` - Verifica la disponibilidad del sistema

## Pruebas

1. Instalar Go 1.24.4
2. `cd users`
3. Ejecutar `go mod download`
4. Ejecutar `sh scripts/test.sh`

Lo anterior ejecutará pruebas unitarias a las principales capas del sistema (http, repository y service), y medirá el porcentaje de coverage para cada una.

## Autor

- Nicolás Cárdenas - [ne.cardenas@uniandes.edu.co](mailto:ne.cardenas@uniandes.edu.co)
