from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, Numeric, Enum as SQLEnum, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from app.core.database import Base
from app.models.vehicle import VehicleStatus, UserRole, ReservationStatus

class Customer(Base):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(255))
    last_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), index=True)
    phone: Mapped[str] = mapped_column(String(50), index=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    preferred_language: Mapped[str] = mapped_column(String(10), default="fr")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

class Reservation(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reservation_code: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    pickup_location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    return_location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    pickup_datetime: Mapped[datetime] = mapped_column(DateTime)
    return_datetime: Mapped[datetime] = mapped_column(DateTime)
    status: Mapped[ReservationStatus] = mapped_column(SQLEnum(ReservationStatus), default=ReservationStatus.DRAFT)
    subtotal: Mapped[float] = mapped_column(Numeric)
    discount: Mapped[float] = mapped_column(Numeric, default=0.0)
    extras_total: Mapped[float] = mapped_column(Numeric, default=0.0)
    delivery_fee: Mapped[float] = mapped_column(Numeric, default=0.0)
    total: Mapped[float] = mapped_column(Numeric)
    currency: Mapped[str] = mapped_column(String(10), default="MAD")
    notes: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    customer: Mapped["Customer"] = relationship("Customer")
    vehicle: Mapped["Vehicle"] = relationship("Vehicle")

class Extra(Base):
    __tablename__ = "extras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price_type: Mapped[str] = mapped_column(String(50)) # PER_DAY, PER_RENTAL, FIXED
    price: Mapped[float] = mapped_column(Numeric)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class ReservationExtra(Base):
    __tablename__ = "reservation_extras"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    reservation_id: Mapped[int] = mapped_column(ForeignKey("reservations.id"))
    extra_id: Mapped[int] = mapped_column(ForeignKey("extras.id"))
    quantity: Mapped[int] = mapped_column(Integer, default=1)
    price_at_booking: Mapped[float] = mapped_column(Numeric)

    reservation: Mapped["Reservation"] = relationship("Reservation")
    extra: Mapped["Extra"] = relationship("Extra")

class PricingRule(Base):
    __tablename__ = "pricing_rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"), nullable=True) # Null means global rule
    category: Mapped[str] = mapped_column(String(50), nullable=True)
    min_days: Mapped[int] = mapped_column(Integer)
    max_days: Mapped[int] = mapped_column(Integer, nullable=True)
    price_modifier: Mapped[float] = mapped_column(Numeric) # multiplier or fixed offset
    modifier_type: Mapped[str] = mapped_column(String(50)) # PERCENTAGE, FIXED
    active: Mapped[bool] = mapped_column(Boolean, default=True)
