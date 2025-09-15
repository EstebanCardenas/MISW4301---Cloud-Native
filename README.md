# Proyecto grupo 1

## Tabla de contenido

- [Proyecto grupo 1](#proyecto-grupo-1)
  - [Tabla de contenido](#tabla-de-contenido)
  - [Estructura del Proyecto](#estructura-del-proyecto)
  - [Archivo de configuración](#archivo-de-configuración)
  - [Estructura de cada aplicación](#estructura-de-cada-aplicación)
  - [Despliegue de la aplicación completa](#despliegue-de-la-aplicación-completa)
    - [Requisitos](#requisitos)
    - [1. Creación de imágenes](#1-creación-de-imágenes)
    - [2. Cargar imágenes a Minikube](#2-cargar-imágenes-a-minikube)
    - [3. Ejecutar en Minikube](#3-ejecutar-en-minikube)
    - [4. Obtener url de un servicio](#4-obtener-url-de-un-servicio)

## Estructura del Proyecto

```
.
├── github/
│   └── workflows/          # Pipelines del repositorio
├── docs/                   # Archivos de documentación técnica
├── k8s/                    # Archivos para despliegue en k8s
├── offers_app              # Aplicación de ofertas
├── posts_app               # Aplicación de publicaciones
├── routes_app              # Aplicación de trayectos
├── users_app               # Aplicación de usuarios
├── scores_app              # Aplicación de scores
├── rf003                   # Aplicación para requerimiento rf003
├── rf004                   # Aplicación para requerimiento rf004
├── rf005                   # Aplicación para requerimiento rf005
├── vale.ini                # Configuración para Vale.
├── config.yaml             # Configuración del repositorio.
├── Makefile                # Scripts para evaluación.
└── README.md               
```

1. **github/workflows**: archivos de ci para validaciones del proyecto.
   * `ci_evaluador_entrega2_k8s.yml` verifica configuración de k8s y ejecuta pruebas sobre cada aplicación.
   * `ci_evaluador_unit.yml` ejecuta pruebas unitarias.
2. **k8s**: archivos de configuración y despliegue de las aplicaciones.
3. **docs**: archivos de la documentación técnica.
4. **<aplicación>**: una carpeta por cada aplicación (offers, posts, routes, users, scores, rf003, rf004, rf005). 
5. **makefile**: el archivo `makefile` es utilizado por los pipelines evaluadores, y contiene scripts de utilidad para construir la infraestructura del proyecto.

## Archivo de configuración

El archivo `config.yaml` contiene la configuración que se usa en los pipelines para evaluar la entrega.

## Estructura de cada aplicación

Para cada aplicación creada, dirigirse a su documentación respectiva para realizar el despliegue
1. [offers](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/offers_app)
2. [posts](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/posts_app)
3. [routes](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/routes_app)
4. [users](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/users_app)
5. [scores](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/scores_app)
6. [rf003](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/rf003)
7. [rf004](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/rf004)
8. [rf005](https://github.com/MISW-4301-Desarrollo-Apps-en-la-Nube/s202514-proyecto-grupo1/tree/main/rf005)

## Despliegue de la aplicación completa

### Requisitos
- terraform
- kubectl
- docker
- aws CLI
- helm
- make

### 1. Creación de infraestructura
```
bash scripts/build_stacks.sh
```

### 2. Configuración base de datos

<p>
Entrar a los siguientes archivos:
</p>
<ul>
  <li>k8s/offers-app-deployment</li>
  <li>k8s/posts-app-deployment</li>
  <li>k8s/routes-app-deployment</li>
  <li>k8s/scores-app-deployment</li>
  <li>k8s/users-app-deployment</li>
</ul>

Y actualizar el secreto del host de la base de datos en cada uno de ellos:

![alt text](./docs/readme-assets/secret-config.png)

### 3. Construir y subir imágenes

```
bash scripts/build_images.sh
```

### 4. Aplicar deployments
```bash
bash scripts/build_k8s.sh
```

Puede que en este paso no se haya podido aplicar la configuración del ingress. Si se obtiene un mensaje de error relacionado a esto, correr el siguiente comando:

`kubectl apply -f ./k8s`
