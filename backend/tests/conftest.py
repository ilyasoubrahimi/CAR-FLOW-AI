import asyncio
import sys
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.config import settings

# Use a separate test database to avoid mutating production data
TEST_DATABASE_URL = settings.DATABASE_URL.replace('postgresql://', 'postgresql+asyncpg://')
if 'localhost' in TEST_DATABASE_URL:
    TEST_DATABASE_URL = TEST_DATABASE_URL.replace('marrakech_drive', 'marrakech_drive_test')

@pytest_asyncio.fixture(scope='session')
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope='function')
async def db_session(test_engine):
    async with test_engine.begin() as conn:
        async with AsyncSession(bind=conn, expire_on_commit=False) as session:
            yield session
            await session.rollback()

@pytest_asyncio.fixture(scope='session')
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac

@pytest.fixture(autouse=True)
async def setup_test_data(db_session):
    from app.models.vehicle import Vehicle, Company, Location

    # 1. Seed Company
    company = Company(name='Marrakech Drive Test', email='test@md.com', phone='123456789', address='Test Address')
    db_session.add(company)
    await db_session.flush() # Get company.id

    # 2. Seed Location
    location = Location(
        name='Marrakech Airport',
        slug='marrakech-airport',
        city='Marrakech',
        address='Airport Road',
        type='AIRPORT',
        latitude=31.6,
        longitude=-8.0
    )
    # Note: The model in vehicle.py for Location doesn't show company_id, but usually it exists.
    # If it doesn't, this is fine. If it does, we'd set it here.
    db_session.add(location)
    await db_session.flush() # Get location.id

    # 3. Seed Vehicle
    vehicle = Vehicle(
        brand='Porsche',
        model='911 Carrera',
        year=2024,
        category='Luxury',
        transmission='Automatic',
        fuel='Petrol',
        seats=2,
        luggage=1,
        daily_price=1500.0,
        status='AVAILABLE',
        slug='porsche-911-carrera',
        location_id=location.id
    )

    db_session.add(vehicle)
    await db_session.commit()
