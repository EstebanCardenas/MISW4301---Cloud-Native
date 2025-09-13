from datetime import datetime
from uuid import UUID


class Route:

    def __init__(
        self,
        id: UUID,
        flight_id: str,
        source_airport_code: str,
        source_country: str,
        destiny_airport_code: str,
        destiny_country: str,
        bag_cost: int,
        planned_start_date: datetime,
        planned_end_date: datetime,
        created_at: datetime,
        updated_at: datetime,
    ):
        self.id = id
        self.flight_id = flight_id
        self.source_airport_code = source_airport_code
        self.source_country = source_country
        self.destiny_airport_code = destiny_airport_code
        self.destiny_country = destiny_country
        self.bag_cost = bag_cost
        self.planned_start_date = planned_start_date
        self.planned_end_date = planned_end_date
        self.created_at = created_at
        self.updated_at = updated_at
