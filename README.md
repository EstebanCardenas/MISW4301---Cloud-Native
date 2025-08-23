# Proyecto grupo 1

## Tabla de contenido

- [Proyecto grupo 1](#proyecto-grupo-1)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Archivo de configuración](#archivo-de-configuración)
  - [Estructura de cada aplicación](#estructura-de-cada-aplicación)

## Estructura del Proyecto

```
.
├── github/
│   └── workflows/          # Pipelines del repositorio
├── docs/                   # Archivos de documentación técnica
├── k8s/                    # Archivos para despliegue en k8s
├── offers_app              # Aplicación de trayectos
├── posts_app               # Aplicación de usuarios
├── routes_app               # Aplicación de usuarios
├── users_app               # Aplicación de usuarios
├── vale.ini                # Configuración para Vale.
├── config.yaml             # Configuración del repositorio.
├── Makefile                # Scripts para evaluación.
└── README.md               
```

1. **github/workflows**: archivos de ci para validaciones del proyecto.
   * `ci_evaluador_entrega1_k8s.yml` verifica configuración de k8s y ejecuta pruebas sobre cada aplicación.
   * `ci_evaluador_entrega1_docs.yml` verifica que los diagramas de la documentación contengan los componentes esperados, hace una revisión gramática sobre el contenido del markdown.
   * `ci_evaluador_unit.yml` ejecuta pruebas unitarias.
2. **k8s**: archivos de configuración y despliegue de las aplicaciones.
3. **docs**: archivos de la documentación técnica.
4. **<aplicación>**: una carpeta por cada aplicación (offers, posts, routes, users). 
5. **makefile**: el archivo `makefile` es utilizado por los pipelines evaluadores.

## Archivo de configuración

El archivo `config.yaml` contiene la configuración que se usa en los pipelines para evaluar la entrega.

## Estructura de cada aplicación

Para cada aplicación creada, dirigirse a su documentación respectiva para realizar el despliegue
1. [offers](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/offers_app)
2. [posts](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/posts_app)
3. [routes](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/routes_app)
4. [users](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/users_app)