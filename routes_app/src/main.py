from typing import Optional
from uuid import UUID

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, PlainTextResponse
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 🎯 Interceptar errores de validación de Pydantic y devolver 400 en vez de 422
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST, content={"detail": exc.errors()}
    )


@app.post(
    "/routes",
    response_model=schemas.RouteCreatedResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_route(db=db, route=route)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_412_PRECONDITION_FAILED, content=e.args[0]
        )


@app.get("/routes", response_model=list[schemas.Route])
def read_routes(
    skip: int = 0,
    limit: int = 100,
    flight: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_routes(db, skip=skip, limit=limit, flight=flight)


@app.get("/routes/count")
def get_routes_count(db: Session = Depends(get_db)):
    count = crud.get_routes_count(db)
    return {"count": count}


@app.get("/routes/ping", response_class=PlainTextResponse)
def ping():
    return "pong"


@app.post("/routes/reset")
def reset_routes(db: Session = Depends(get_db)):
    crud.reset_routes(db)
    return {"msg": "Todos los datos fueron eliminados"}


@app.get("/routes/{route_id}", response_model=schemas.Route)
def read_route(route_id: UUID, db: Session = Depends(get_db)):
    db_route = crud.get_route(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return db_route


@app.delete("/routes/{route_id}")
def delete_route(route_id: UUID, db: Session = Depends(get_db)):
    db_route = crud.delete_route(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail="Route not found")
    return {"msg": "el trayecto fue eliminado"}
