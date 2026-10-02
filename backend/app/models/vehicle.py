from sqlalchemy import String, Integer, Boolean, ForeignKey, Text, DateTime, Numeric, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum
from app.core.database import Base

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    STAFF = "STAFF"

class VehicleStatus(enum.Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    RENTED = "RENTED"
    MAINTENANCE = "MAINTENANCE"
    INACTIVE = "INACTIVE"

class LocationType(enum.Enum):
    AIRPORT = "AIRPORT"
    AGENCY = "AGENCY"
    HOTEL = "HOTEL"
    CUSTOM = "CUSTOM"

class ReservationStatus(enum.Enum):
    DRAFT = "DRAFT"
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class Company(Base):
    __tablename__ = "companies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    logo_url: Mapped[str] = mapped_column(String(512), nullable=True)
    primary_color: Mapped[str] = mapped_column(String(20), default="#000000")
    secondary_color: Mapped[str] = mapped_column(String(20), default="#FFFFFF")
    phone: Mapped[str] = mapped_column(String(50))
    whatsapp_number: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    address: Mapped[str] = mapped_column(Text)
    default_currency: Mapped[str] = mapped_column(String(10), default="MAD")
    timezone: Mapped[str] = mapped_column(String(50), default="Africa/Casablanca")
    supported_languages: Mapped[str] = mapped_column(String(255), default="fr,en,ar")
    booking_rules: Mapped[str] = mapped_column(Text, nullable=True)
    cancellation_policy: Mapped[str] = mapped_column(Text, nullable=True)
    airport_pickup_available: Mapped[bool] = mapped_column(Boolean, default=True)
    hotel_delivery_available: Mapped[bool] = mapped_column(Boolean, default=True)

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    full_name: Mapped[str] = mapped_column(String(255))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.STAFF)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    type: Mapped[LocationType] = mapped_column(SQLEnum(LocationType))
    address: Mapped[str] = mapped_column(Text)
    city: Mapped[str] = mapped_column(String(100))
    latitude: Mapped[float] = mapped_column(Numeric)
    longitude: Mapped[float] = mapped_column(Numeric)
    active: Mapped[bool] = mapped_column(Boolean, default=True)

class Vehicle(Base):
    __tablename__ = "vehicles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    slug: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    brand: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))
    year: Mapped[int] = mapped_column(Integer)
    category: Mapped[str] = mapped_column(String(50))
    transmission: Mapped[str] = mapped_column(String(50))
    fuel: Mapped[str] = mapped_column(String(50))
    seats: Mapped[int] = mapped_column(Integer)
    luggage: Mapped[int] = mapped_column(Integer)
    air_conditioning: Mapped[bool] = mapped_column(Boolean, default=True)
    description: Mapped[str] = mapped_column(Text)
    short_description: Mapped[str] = mapped_column(String(512))
    daily_price: Mapped[float] = mapped_column(Numeric)
    status: Mapped[VehicleStatus] = mapped_column(SQLEnum(VehicleStatus), default=VehicleStatus.AVAILABLE)
    featured: Mapped[bool] = mapped_column(Boolean, default=False)
    location_id: Mapped[int] = mapped_column(ForeignKey("locations.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())

    location: Mapped["Location"] = relationship("Location")
    images: Mapped[list["VehicleImage"]] = relationship("VehicleImage", back_populates="vehicle")

class VehicleImage(Base):
    __tablename__ = "vehicle_images"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    vehicle_id: Mapped[int] = mapped_column(ForeignKey("vehicles.id"))
    url: Mapped[str] = mapped_column(String(512))
    alt: Mapped[str] = mapped_column(String(255), nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, default=0)
    is_primary: Mapped[bool] = mapped_column(Boolean, default=False)

    vehicle: Mapped["Vehicle"] = relationship("Vehicle", back_populates="images")
