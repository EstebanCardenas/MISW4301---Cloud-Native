# Routes app

Esta app está desarrollado en FastAPI que implementa una arquitectura hexagonal (también conocida como puertos y adaptadores) para gestionar la entidad Pet. La aplicación se ejecuta haciendo uso de docker y puede ser ejecutada directamente en su ambiente o haciendo uso de k8s.

## Índice

1. [Estructura](#estructura)
2. [Ejecución](#ejecución)
3. [Uso](#uso)
4. [Pruebas](#pruebas)
5. [Autor](#autor)

## Requisitos

- Python 3.13
- Poetry version 2.1.4
- Docker
- Postman

## Estructura

```
.
├── src/
│   ├── domain/             # Capa de dominio
│   │   ├── models/         # Modelos de dominio
│   │   ├── ports/          # Puertos (interfaces)
│   │   └── use_cases/      # Casos de uso
│   ├── adapters/           # Capa de adaptadores
│   │   └── database/       # Adaptador de base de datos
│   └── entrypoints/        # Puntos de entrada
│       └── api/            # API REST
├── tests/                  # Pruebas
├── Dockerfile              # Configuración de Docker
├── pyproject.toml          # Configuración de Poetry
└── README.md               # Este archivo
```

### Carpeta src

Esta carpeta contiene el código y la lógica de la aplicación que permite exponer el API y puede integrar otras aplicaciones o componentes si lo requiere.

#### Domain

Carpeta con la lógica de la aplicación. Si tu aplicación está diseñada para cocinar una receta, esta carpeta es la cocina. 

- `/domain/models`: Contiene las clases que representan las entidades necesarias para los casos de uso de la aplicación. Comúnmente estos modelos son usados para el almacenamiento en la base de datos, pero no deben confundirse, estas clases no deben estar acopladas a una base de datos en específico y solo representan las entidades que se van a manipular en los casos de uso. Será responsabilidad de los adaptadores transformarlas y almacenarlas en una determinada base de datos. En este ejemplo los modelos estarán soportados haciendo uso de pydantic por facilidad de validación e integración con FastAPI.

```python
# domain/models/pet.py
class Pet(BaseModel):
    """Pet domain model."""

    id: int | None = None
    name: str = Field(min_length=1, description="Name cannot be empty")
    type: PetType
    age: int = Field(gt=0, description="Age must be greater than 0")
    owner_name: str = Field(min_length=1, description="Owner name cannot be empty")
```

- `/domain/ports`: Contiene las interfaces que habilitan la interacción con componentes o lógica externa. Estas clases no son implementaciones sino únicamente el "template" que deben seguir nuestras integraciones. Esto permite desacoplar la implementación, habilitando que se pueda reemplazar fácilmente los componentes con los que se integra la aplicación, siempre y cuando se respecte la definición de las interfaces. En este proyecto encontrará que se hace uso de una clase llamada [Repository](https://martinfowler.com/eaaCatalog/repository.html) la cual sigue un patrón que es comúnmente usado cuando el puerto es usado para almacenamiento de una entidad. Sin embargo, los puertos pueden seguir otros patrones para interactuar con otros componentes, por ejemplo notificaciones.

```python
# domain/ports/pet_repository_port.py
class PetRepositoryPort(ABC):
    """Pet repository interface."""

    @abstractmethod
    def create(self, pet: Pet) -> Pet:
        """Create a new pet."""
        pass
    ...

# another example
class NotificationDeliveryPort(ABC):
    """Designed to send notifications."""

    @abstractmethod
    def send(self, payload:Dict[str, str], title:str) -> bool:
        """Sends a notification."""
        pass
    ...
```

- `/domain/use_cases`: Contiene los casos de uso de la aplicación, almacenar, consultar, modificar, borrar o cualquier otra funcionalidad. Todos los casos de usos deben compartir el mismo contrato. Para ello deben extender de una interfaz que define como es el comportamiento de los casos de uso, esta interfaz resulta ser clave para permitir que los entrypoints de la aplicación puedan interactuar con los casos de uso sin generar acoplamiento.

```python
# domain/use_cases/base_use_case.py
class BaseUseCase(ABC):
    """Base use case class."""

    @abstractmethod
    def execute(self, *args, **kwargs):
        """Execute the use case."""
        pass

# domain/use_cases/create_pet_use_case.py
class CreatePetUseCase(BaseUseCase):
    """Use case for saving a pet."""

    def __init__(self, pet_repository: PetRepositoryPort):
        self.pet_repository = pet_repository

    def execute(self, pet: Pet) -> Pet:
        """Create a new pet."""
        return self.pet_repository.create(pet)
```
#### Adapters

En la carpeta adapters se encuentra la implementación de los puertos definidos en la carpeta de ports. En este proyecto de ejemplo se encuentra una implementación de un almacenamiento en memoria, pero usted puede seguir el mismo schema si quiere realizar una implementación para almacenar en una base de datos.

```python
# adapters/memory/pet_repository_adapter.py
class InMemoryPetRepositoryAdapter(PetRepositoryPort):
    """In memory implementation of PetRepository."""

    memory_store: Dict[int, Pet] = {}

    def sequence(self) -> int:
        """Generate a new sequence number."""
        return len(self.memory_store) + 1

    def create(self, pet: Pet) -> Pet:
        """Create a new pet."""
        pet.id = self.sequence()
        self.memory_store[pet.id] = pet
        return pet
    ...

# Another example
# Disclaimer: We suggest using Async Await if you plan to use SQL databases
class SQLAlchemyPetRepositoryAdapter(PetRepositoryPort):
    """SQL implementation of PetRepository."""
    def __init__(self, session: Session):
        self.session = session

    def create(self, pet: Pet) -> Pet:
        pet_model = pet_entity_to_model(pet)
        self.session.add(pet_model)
        self.session.commit()
        self.session.refresh(pet_model)
        return pet_model_to_entity(pet_model)
    ...
```

#### Entrypoints

Contiene los archivos que servirán como punto de acceso a la aplicación; también podrían considerarse como puertos de ingreso. En esta carpeta se encuentran las funciones o clases que permiten interactuar con los casos de uso. La implementación dependerá principalmente de la tecnología utilizada, cuando se trabaja con FastAPI normalmente se habla de Routers, mientras en Flask se encuentran los Blueprints.

En este proyecto se hace uso de routers donde se definen las rutas y los métodos HTTP que se soportan. Si usted quiere agregar nuevas rutas, debe agregar otro archivo router o modificar el actual siguiendo el mismo patrón.

```python
router = APIRouter(prefix="/pets")

@router.get("/ping", response_class=PlainTextResponse)
def health_check():
    """Healthcheck endpoint."""
    return "pong"
```

Posteriormente debe agregar el router a la aplicación en el archivo `main.py`

```python
app = FastAPI(title=Settings.app_name)
app.include_router(pet_router)
```

#### Configuración y ensamble

- `config.py`: En este archivo se encuentran las funciones que permiten leer las variables de ambiente o constantes que se usan en todo el proyecto. Es una buena práctica consolidar el manejo de las variables de ambiente y constantes a un solo archivo, facilita las pruebas y la mantenibilidad.
- `assembly.py`: Este archivo contiene las funciones que realizan la inyección de dependencias. Como ha podido ver en todos los ejemplos previos, las asociaciones entre las clases y funciones se realizan por medio de interfaces, ninguna clase conoce o usa una implementación en particular. Es en este paquete donde se instancian las implementaciones que se van a usar y las cuales son usadas por cada router:

```python
# assembly.py
repository: InMemoryPetRepositoryAdapter = InMemoryPetRepositoryAdapter()

def build_create_pet_use_case() -> BaseUseCase:
    """Get create pet use case."""
    return CreatePetUseCase(repository)
...

# entrypoints/api/routers/pet_router.py
@router.post("/", response_model=Pet)
def create_pet(
    pet: Pet, use_case: BaseUseCase = Depends(build_create_pet_use_case)
):
    """Create a new pet."""
    return use_case.execute(pet)
```

#### Errores

En el proyecto se encuentra el archivo `errors.py` el cual está diseñado para albergar todas las clases de excepciones personalizadas que se creen en el proyecto. Recomendamos crear sus propias clases de excepción para tener mayor control del flujo del programa.

```python
class PetNotFoundError(Exception):
    """Exception raised when a pet is not found."""
    pass
```

Haciendo uso de un handler de excepciones personalizado, puede indicarle a FastAPI que responda un error en particular cuando reciba este tipo de excepciones en un router.

```python
app = FastAPI(title=Settings.app_name)

@app.exception_handler(PetNotFoundError)
def pet_not_found_exception_handler(request: Request, exc: PetNotFoundError):
    return JSONResponse(
        status_code=404,
        content={"detail": exc.message},
    )
...
```

### Configuración

Este proyecto hace uso de [poetry](https://python-poetry.org/) para la gestión de dependencias y configuración de algunas librerías usadas en el proyecto. Encontrará la configuración en el archivo `pyproject.toml` el cuál ya es un estandar para la configuración de proyectos en Python. [Documentación](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).


## Ejecución

### 1. Instale las dependencias:
```bash
poetry install

# Si no existe el archivo poetry.lock ejecute primero
# poetry lock
```
Poetry instalará todas las dependencias en un ambiente virtual gestionado por Poetry.

### 2. Ejecución

Dado que todas las dependencias están instaladas en un ambiente virtualizado y gestionado por Poetry es necesario correr el servidor haciendo uso de Poetry:
```bash
PYTHONPATH=$(pwd)/src poetry run uvicorn src.main:app --host 0.0.0.0 --port 9000
```

El API estará disponible en `http://localhost:9000`

Cargue el archivo `routes_app/tests/api/pets.postman_collection.json` en su Postman y reemplace la variable `baseUrl` por la url.

Ejecute las pruebas y verifique que se completa correctamente.

#### Ejecutar en Docker

```bash
APP_VERSION = ... # use la misma versión del documento pyproject.toml
APP_NAME = ... # use el mismo definido en el documento pyproject.toml
docker build --rm --platform linux/amd64 -t ${APP_NAME}:${APP_VERSION} -f Dockerfile --target runner --label version=${APP_VERSION} .

docker run --platform linux/amd64 -p 9000:9000 ${APP_NAME}:${APP_VERSION}
```

#### Ejecutar en minikube

Después de haber creado la imagen haciendo uso de docker, ejecute:

```bash
minikube start --cpus=2 --memory=3g --cni calico

#make mkbuild
minikube image load ${APP_NAME}:${APP_VERSION}

kubectl apply -f k8s
minikube service pets-service
```

Minikube asignará un puerto para que pueda acceder a su servicio. Puede usarlo en su browser o en postman.

## Uso

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

Las pruebas de integración se realizan por medio de Postman y newman. Encontrará un archivo de colección de postman en la carpeta `tests/api/` el cuál puede cargar en su aplicación de postman de manera local. Posteriormente puede ejecutar `Run collection` para verificar que la aplicación está funcionando correctamente.

## Autor

- Germán Martínez - [gd.martinez@uniandes.edu.co](mailto:gd.martinez@uniandes.edu.co)