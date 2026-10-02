from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional
from datetime import datetime

class SeedVehicle(BaseModel):
    brand: str
    model: str
    year: int
    category: str
    transmission: str
    fuel: str
    seats: int
    luggage: int
    daily_price: Decimal
    slug: str

SEED_VEHICLES = [
    SeedVehicle(brand="Peugeot", model="208", year=2023, category="Economy", transmission="Automatic", fuel="Petrol", seats=5, luggage=2, daily_price=Decimal("350"), slug="peugeot-208"),
    SeedVehicle(brand="Renault", model="Clio", year=2023, category="Economy", transmission="Automatic", fuel="Petrol", seats=5, luggage=2, daily_price=Decimal("350"), slug="renault-clio"),
    SeedVehicle(brand="Dacia", model="Sandero", year=2022, category="Economy", transmission="Manual", fuel="Petrol", seats=5, luggage=2, daily_price=Decimal("300"), slug="dacia-sandero"),
    SeedVehicle(brand="Dacia", model="Duster", year=2023, category="SUV", transmission="Automatic", fuel="Diesel", seats=5, luggage=4, daily_price=Decimal("500"), slug="dacia-duster"),
    SeedVehicle(brand="Peugeot", model="3008", year=2023, category="SUV", transmission="Automatic", fuel="Diesel", seats=5, luggage=4, daily_price=Decimal("700"), slug="peugeot-3008"),
    SeedVehicle(brand="Volkswagen", model="Golf", year=2023, category="Compact", transmission="Automatic", fuel="Petrol", seats=5, luggage=3, daily_price=Decimal("600"), slug="vw-golf"),
    SeedVehicle(brand="BMW", model="Série 1", year=2024, category="Premium", transmission="Automatic", fuel="Petrol", seats=5, luggage=2, daily_price=Decimal("900"), slug="bmw-serie-1"),
    SeedVehicle(brand="Mercedes-Benz", model="A-Class", year=2024, category="Premium", transmission="Automatic", fuel="Petrol", seats=5, luggage=2, daily_price=Decimal("950"), slug="mercedes-a-class"),
    SeedVehicle(brand="Range Rover", model="Evoque", year=2023, category="Luxury", transmission="Automatic", fuel="Diesel", seats=5, luggage=3, daily_price=Decimal("1500"), slug="range-rover-evoque"),
    SeedVehicle(brand="Mercedes-Benz", model="GLC", year=2023, category="Luxury", transmission="Automatic", fuel="Diesel", seats=5, luggage=4, daily_price=Decimal("1800"), slug="mercedes-glc"),
]
