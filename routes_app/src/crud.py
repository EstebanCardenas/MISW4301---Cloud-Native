from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from . import models, schemas


def get_routes(
    db: Session, skip: int = 0, limit: int = 100, flight: Optional[str] = None
):
    query = db.query(models.Route)
    if flight:
        query = query.filter(models.Route.flightId == flight)
    return query.offset(skip).limit(limit).all()


def get_route(db: Session, route_id: UUID):
    return db.query(models.Route).filter(models.Route.id == route_id).first()


def create_route(db: Session, route: schemas.RouteCreate):
    # 1. Validar que el flightId no exista ya
    existing_route = (
        db.query(models.Route)
        .filter(models.Route.flightId == str(route.flightId))
        .first()
    )
    if existing_route:
        raise ValueError({"msg": "El flightId ya existe"})

    # 2. Validar fechas
    now = datetime.now(timezone.utc)
    start = route.plannedStartDate
    end = route.plannedEndDate
    if start < now or end < now:
        raise ValueError({"msg": "Las fechas del trayecto no son válidas"})
    if start >= end:
        raise ValueError({"msg": "Las fechas del trayecto no son válidas"})

    # 3. Crear registro
    db_route = models.Route(**route.model_dump())
    db.add(db_route)
    db.commit()
    db.refresh(db_route)

    # Retornamos solo los campos requeridos
    return {"id": db_route.id, "createdAt": db_route.createdAt}


def delete_route(db: Session, route_id: int):
    db_route = db.query(models.Route).filter(models.Route.id == route_id).first()
    if db_route:
        db.delete(db_route)
        db.commit()
    return db_route


def get_routes_count(db: Session) -> int:
    return db.query(models.Route).count()


def reset_routes(db: Session):
    db.query(models.Route).delete()
    db.commit()
