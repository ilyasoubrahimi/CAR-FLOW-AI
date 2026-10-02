import asyncio
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import AsyncSessionLocal
from app.core.seed import SEED_VEHICLES
from app.models.vehicle import Vehicle, Location, Company, User
from app.core.security import get_password_hash

async def seed_database():
    # CRITICAL: Admin password must be provided via environment variable
    admin_password = os.environ.get("ADMIN_SEED_PASSWORD")
    if not admin_password:
        print("ERROR: ADMIN_SEED_PASSWORD environment variable is required to seed the database.")
        return

    async with AsyncSessionLocal() as session:
        # 1. Seed Company (Idempotent)
        res_company = await session.execute(select(Company))
        company = res_company.scalars().first()
        if not company:
            company = Company(
                name="Marrakech Drive",
                phone="+212600000000",
                whatsapp_number="+212600000000",
                email="contact@marrakechdrive.com",
                address="Av Mohamed V, Marrakech, Morocco",
                default_currency="MAD"
            )
            session.add(company)
            await session.flush()
            print("Company seeded.")
        else:
            print("Company already exists, skipping.")

        # 2. Seed Location (Idempotent)
        res_loc = await session.execute(select(Location).where(Location.slug == "marrakech-agency"))
        location = res_loc.scalar_one_or_none()
        if not location:
            location = Location(
                name="Marrakech Agency",
                slug="marrakech-agency",
                type="AGENCY",
                address="Av Mohamed V, Marrakech",
                city="Marrakech",
                latitude=31.6295,
                longitude=-7.9811
            )
            session.add(location)
            await session.flush()
            print("Location seeded.")
        else:
            print("Location already exists, skipping.")

        # 3. Seed Admin User (Idempotent)
        res_user = await session.execute(select(User).where(User.username == "admin"))
        admin = res_user.scalar_one_or_none()
        if not admin:
            admin = User(
                username="admin",
                hashed_password=get_password_hash(admin_password),
                email="admin@marrakechdrive.com",
                full_name="Super Admin",
                role="ADMIN"
            )
            session.add(admin)
            print("Admin user seeded.")
        else:
            print("Admin user already exists, skipping.")

        # 4. Seed Vehicles (Idempotent by slug)
        for v in SEED_VEHICLES:
            res_v = await session.execute(select(Vehicle).where(Vehicle.slug == v.slug))
            existing_v = res_v.scalar_one_or_none()
            if not existing_v:
                vehicle = Vehicle(
                    brand=v.brand,
                    model=v.model,
                    year=v.year,
                    category=v.category,
                    transmission=v.transmission,
                    fuel=v.fuel,
                    seats=v.seats,
                    luggage=v.luggage,
                    daily_price=v.daily_price,
                    slug=v.slug,
                    location_id=location.id,
                    description=f"Premium {v.brand} {v.model} for your journey in Marrakech.",
                    short_description=f"Elegant {v.category} vehicle."
                )
                session.add(vehicle)

        await session.commit()
        print("Seed process completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_database())
