from datetime import datetime, timezone

from sqlalchemy.orm import Session

from src.models.internal.route import Route


def validateRoute(db: Session, route: Route) -> str | None:
    # 1. Validar que el flightId no exista ya
    existing_route = (
        db.query(Route).filter(Route.flightId == str(route.flightId)).first()
    )
    if existing_route:
        return "El flightId ya existe"

    # 2. Validar fechas
    now = datetime.now(timezone.utc)
    start = route.plannedStartDate
    end = route.plannedEndDate
    if start < now or end < now:
        return "Las fechas del trayecto no son válidas"
    if start >= end:
        return "Las fechas del trayecto no son válidas"

    return None
