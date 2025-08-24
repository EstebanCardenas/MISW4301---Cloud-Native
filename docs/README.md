# Grupo
Nombre: Alfa buena maravilla onda dinamita escuadrón lobo
Líder: Andrés Donoso

# Integrantes
|      Nombre      |            Correo           |  Usuario GitHub |       Rol       |     Interés     |
|----------------|---------------------------|---------------|---------------|---------------|
|   Andrés Donoso  |  af.donoso@uniandes.edu.co  |    afDonosoD    |     Backend     |   Desarrollo    |
|  Germán Martínez | gd.martinez@uniandes.edu.co |    DavidMS73    |     Backend     |   Desarrollo    |
| Nicolas Cárdenas | ne.cardenas@uniandes.edu.co | EstebanCardenas |     Backend     |   Desarrollo    |
|   Daniel Corzo   | d.corzos@uniandes.edu.co    |   daniel-corzo  |     Backend     |   Desarrollo    |

# Reglas
1. Entrar a las reuniones programadas a tiempo (máximo 5 minutos tarde). 
2. Realizar al menos 2 reuniones semanales, una para planear la semana y otra para revisar lo que se completó en la semana. 
3. Revisar siempre el trabajo hecho por el otro integrante del equipo y dar retroalimentación para que complete lo realizado o se den felicitaciones por el trabajo hecho. 
4. En todos los trabajos grupales el equipo se compromete a aspirar a una nota de 5. 
5. Se definen las siguientes herramientas de colaboración adicionales: Google Docs para edición de documentos, Slack/WhatsApp para preguntas, Zoom para reuniones, Slides para edición de diapositivas. 
6. Comunicar a tiempo algún contratiempo que no permita subirse a las reuniones o cumplir a tiempo una actividad, con el fin de que el equipo brinde el soporte en caso de ser necesario. 

## Vistas de arquitectura

### Vista de información

![Vista de información](./diagrams/entities.png "Vista de información")

### Vista funcional
  
![Vista funcional](./diagrams/components.png "Vista funcional")

### Vista de despliegue

![Vista de despliegue](./diagrams/deployment.png "Vista de despliegue")

### Vista de red

![Vista de red](./diagrams/networks.png "Vista de red")

### Vista de desarrollo

#### Tecnologías
1. Lenguajes: Python / Go - Framework: FastAPI / GIN
2. Librerías de pruebas: pytest y httpx
3. Base de datos: PostgreSQL (producción), SQLite (pruebas)
4. ORM: SQLAlchemy / GORM
5. Serialización/validación: Pydantic
6. Servidor ASGI: Uvicorn
7. Manejo de dependencias: poetry
8.  Despliegue: Docker
