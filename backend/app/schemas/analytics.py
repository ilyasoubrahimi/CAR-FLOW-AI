from pydantic import BaseModel
from typing import List, Dict, Any

class AnalyticsOverview(BaseModel):
    total_reservations: int
    today_reservations: int
    confirmed_reservations: int
    active_rentals: int
    completed_rentals: int
    cancelled_reservations: int
    total_revenue: float
    average_rental_duration: float
    most_booked_vehicles: List[Dict[str, Any]]
    available_vehicles: int
    returning_vehicles: int
