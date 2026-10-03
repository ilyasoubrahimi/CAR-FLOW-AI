import pytest
from httpx import AsyncClient
from app.core import security
from app.models.vehicle import User, UserRole
from app.api.deps import get_db

@pytest.mark.asyncio
async def test_admin_location_crud(client: AsyncClient, db_session):
    # 1. Create Admin User
    admin_user = User(
        username="admin",
        hashed_password=security.get_password_hash("admin123"),
        full_name="Admin User",
        email="admin@md.com",
        role=UserRole.ADMIN
    )
    db_session.add(admin_user)
    await db_session.commit()

    # 2. Login to get token
    login_res = await client.post("/api/v1/auth/login", data={"username": "admin", "password": "admin123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test: Unauthorized Access (no token)
    res = await client.get("/api/v1/locations/")
    assert res.status_code == 401

    # Test: Admin Create Location
    loc_data = {
        "name": "City Center",
        "slug": "city-center",
        "type": "AGENCY",
        "address": "Place Jemaa el-Fna",
        "city": "Marrakech",
        "latitude": 31.6,
        "longitude": -8.0
    }
    res = await client.post("/api/v1/locations/", json=loc_data, headers=headers)
    assert res.status_code == 201
    loc_id = res.json()["id"]

    # Test: Admin List Locations
    res = await client.get("/api/v1/locations/", headers=headers)
    assert res.status_code == 200
    assert len(res.json()) >= 1

    # Test: Admin Delete Location
    res = await client.delete(f"/api/v1/locations/{loc_id}", headers=headers)
    assert res.status_code == 204

@pytest.mark.asyncio
async def test_admin_reservation_list(client: AsyncClient, db_session):
    # Create Admin
    admin_user = User(
        username="admin2",
        hashed_password=security.get_password_hash("admin123"),
        full_name="Admin User 2",
        email="admin2@md.com",
        role=UserRole.ADMIN
    )
    db_session.add(admin_user)
    await db_session.commit()
    
    login_res = await client.post("/api/v1/auth/login", data={"username": "admin2", "password": "admin123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test: Admin List Reservations
    res = await client.get("/api/v1/reservations/", headers=headers)
    assert res.status_code == 200

@pytest.mark.asyncio
async def test_customer_list_forbidden_for_non_admin(client: AsyncClient, db_session):
    # Create Staff User (not Admin)
    staff_user = User(
        username="staff",
        hashed_password=security.get_password_hash("staff123"),
        full_name="Staff User",
        email="staff@md.com",
        role=UserRole.STAFF
    )
    db_session.add(staff_user)
    await db_session.commit()

    login_res = await client.post("/api/v1/auth/login", data={"username": "staff", "password": "staff123"})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test: Staff cannot access customer list
    res = await client.get("/api/v1/customers/", headers=headers)
    assert res.status_code == 403
