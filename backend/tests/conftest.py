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

@pytest_asyncio.fixture(scope='function')
async def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope='function')
async def test_engine(event_loop):
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        from app.core.database import Base
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest_asyncio.fixture(scope='function')
async def db_session(test_engine):
    async with AsyncSession(test_engine, expire_on_commit=False) as session:
        # Override the get_db dependency to use this specific session
        from app.api.deps import get_db
        app.dependency_overrides[get_db] = lambda: session
        try:
            yield session
        finally:
            app.dependency_overrides.clear()


@pytest_asyncio.fixture(scope='session')
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac

@pytest_asyncio.fixture(autouse=True)
async def setup_test_data(db_session):
    from app.models.vehicle import Vehicle, Company, Location
    from app.models.assistant import Conversation

    # 1. Seed Company
    company = Company(name='Marrakech Drive Test', email='test@md.com', phone='123456789', address='Test Address', whatsapp_number='123456789')
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
        description='Test Porsche 911',
        short_description='Luxury Sportscar',
        daily_price=1500.0,
        status='AVAILABLE',
        slug='porsche-911-carrera',
        location_id=location.id
    )

    db_session.add(vehicle)

    # 4. Seed Conversation (Necessary for Assistant tests)
    conversation = Conversation(channel='WEBSITE', status='OPEN')
    db_session.add(conversation)

    await db_session.commit()
