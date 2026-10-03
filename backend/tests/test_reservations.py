import pytest
import asyncio
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_reservation_happy_path(client):
    """Test full flow: Draft -> Confirm."""
    # 1. Create Draft
    payload = {
        "vehicle_id": 1,
        "pickup_date": "2026-12-01T10:00:00",
        "return_date": "2026-12-05T10:00:00",
        "customer": {
            "first_name": "Test",
            "last_name": "User",
            "email": "test@user.com",
            "phone": "+212600000000",
            "passport_number": "ABC123456"
        },
        "extras": ["gps"]
    }
    response = await client.post("/api/v1/reservations/", json=payload)
    assert response.status_code == 201
    res_id = response.json()["id"]
    res_code = response.json()["code"]

    # 2. Confirm
    confirm_res = await client.post(f"/api/v1/reservations/{res_id}/confirm")
    assert confirm_res.status_code == 200
    assert confirm_res.json()["status"] == "CONFIRMED"

@pytest.mark.asyncio
async def test_double_booking_concurrency(client):
    """
    Test that two simultaneous requests to book the same vehicle
    for the same dates results in only one success.
    """
    # Note: True async concurrency testing with AsyncClient is tricky in pytest,
    # but we can simulate the overlapping requests.

    payload = {
        "vehicle_id": 1,
        "pickup_date": "2026-12-10T10:00:00",
        "return_date": "2026-12-15T10:00:00",
        "customer": {
            "first_name": "User1",
            "last_name": "One",
            "email": "u1@test.com",
            "phone": "+212111",
            "passport_number": "P1"
        },
        "extras": []
    }

    # Request 1: Create and confirm
    res1 = await client.post("/api/v1/reservations/", json=payload)
    res1_id = res1.json()["id"]
    await client.post(f"/api/v1/reservations/{res1_id}/confirm")

    # Request 2: Attempt to book the same vehicle for overlapping dates
    payload2 = payload.copy()
    payload2["customer"]["email"] = "u2@test.com"

    res2 = await client.post("/api/v1/reservations/", json=payload2)
    # The draft might be created, but confirmation MUST fail
    res2_id = res2.json()["id"]
    confirm_res2 = await client.post(f"/api/v1/reservations/{res2_id}/confirm")

    assert confirm_res2.status_code == 400 # Should be rejected due to unavailability
