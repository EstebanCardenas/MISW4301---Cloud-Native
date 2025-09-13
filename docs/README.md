# Grupo
Nombre: Alfa buena maravilla onda dinamita escuadrón lobo

Líder: Andrés Donoso

# Integrantes
<table>
  <tr>
    <th>Nombre</th>
    <th>Correo</th>
    <th>Usuario GitHub</th>
    <th>Rol</th>
    <th>Interés</th>
  </tr>
  <tr>
    <td>Andrés Donoso</td>
    <td>af.donoso@uniandes.edu.co</td>
    <td>afDonosoD</td>
    <td>Backend</td>
    <td>Desarrollo</td>
  </tr>
  <tr>
    <td>Germán Martínez</td>
    <td>gd.martinez@uniandes.edu.co</td>
    <td>DavidMS73</td>
    <td>Backend</td>
    <td>Desarrollo</td>
  </tr>
  <tr>
    <td>Nicolas Cárdenas</td>
    <td>ne.cardenas@uniandes.edu.co</td>
    <td>EstebanCardenas</td>
    <td>Backend</td>
    <td>Desarrollo</td>
  </tr>
  <tr>
    <td>Daniel Corzo</td>
    <td>d.corzos@uniandes.edu.co</td>
    <td>daniel-corzo</td>
    <td>Backend</td>
    <td>Desarrollo</td>
  </tr>
</table>

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

<table>
  <tr>
    <th>Componente</th>
    <th>rf003</th>
  </tr>
  <tr>
    <td>Código/Id del componente</td>
    <td>rf003</td>
  </tr>
  <tr>
    <td>Tipo</td>
    <td>Servicio</td>
  </tr>
  <tr>
    <td>Responsabilidad</td>
    <td>Gestionar el requerimiento rf003 e implementar el patrón Sagas</td>
  </tr>
  <tr>
    <td>Consideraciones de diseño</td>
    <td>
      El componente rf003 funciona como orquestador de la transacción entera
    </td>
  </tr>
  <tr>
    <td>Integraciones</td>
    <td>Comunicación síncrona con los microservicios de publicaciones, trayectos y usuarios a través de HTTP</td>
  </tr>
</table>

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

## Requerimientos

<table>
  <tr>
    <th>Requerimieno</th>
    <th>RF003</th>
  </tr>
  <tr>
    <td>Patrón utilizado</td>
    <td>Sagas</td>
  </tr>
  <tr>
    <td>Justificación</td>
    <td>Este patrón permite la implementación de transacciones que involucran varios microservicios. Es necesario aplicar el patrón a este requerimiento ya que se necesita acceder a diferentes microservicios para cumplir con el mismo. Por otra parte, el patrón usa operaciones para revertir las interacciones con cada servicio en caso de que ocurra una falla a fin de mantener la consistencia de los datos.</td>
  </tr>
  <tr>
    <td>Atributos de calidad favorecidos</td>
    <td>
      <ul>
        <li>Consistencia</li>
        <li>Tolerancia a fallos</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Atributos de calidad desfavorecidos</td>
    <td>
      <ul>
        <li>Simplicidad</li>
        <li>Depurabilidad</li>
      </ul>
    </td>
  </tr>
  <tr>
    <td>Componentes involucrados</td>
    <td>
      <ul>
        <li>rf003</li>
        <li>Microservicio publicaciones</li>
        <li>Microservicio trayectos</li>
        <li>Microservicio usuarios</li>
      </ul>
    </td>
  </tr>
</table>

#### Diagrama de proceso

<img src="./diagrams/rf003-flow.jpg" alt="Diagrama de procesos rf003">
