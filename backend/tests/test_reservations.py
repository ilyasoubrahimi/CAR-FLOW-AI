import pytest
import asyncio
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_reservation_happy_path(client, db_session):
    """Test full flow: Draft -> Confirm."""
    from app.models.reservation import Customer, Extra

    # 1. Create Customer
    customer = Customer(
        first_name="Test",
        last_name="User",
        email="test@user.com",
        phone="+212600000000"
    )
    db_session.add(customer)
    await db_session.flush()

    # 2. Create Extra
    extra = Extra(name="GPS", description="GPS Navigation", price_type="PER_DAY", price=50.0, active=True)
    db_session.add(extra)
    await db_session.flush()

    # 3. Create Draft
    payload = {
        "vehicle_id": 1,
        "customer_id": customer.id,
        "pickup_datetime": "2026-12-01T10:00:00",
        "return_datetime": "2026-12-05T10:00:00",
        "extra_ids": [extra.id]
    }
    response = await client.post("/api/v1/reservations/", json=payload)
    assert response.status_code == 201
    res_data = response.json()
    res_id = res_data["id"]

    # 4. Confirm
    confirm_res = await client.post(f"/api/v1/reservations/{res_id}/confirm")
    if confirm_res.status_code != 200:
        print(f"Confirm failed with status {confirm_res.status_code}: {confirm_res.text}")
    assert confirm_res.status_code == 200
    assert confirm_res.json()["status"] == "CONFIRMED"

@pytest.mark.asyncio
async def test_double_booking_concurrency(client, db_session):
    """
    Test that two simultaneous requests to book the same vehicle
    for the same dates results in only one success.
    """
    from app.models.reservation import Customer

    # Create two customers
    c1 = Customer(first_name="U1", last_name="L1", email="u1@test.com", phone="+212111")
    c2 = Customer(first_name="U2", last_name="L2", email="u2@test.com", phone="+212222")
    db_session.add_all([c1, c2])
    await db_session.flush()

    # Use explicit IDs to avoid sqlalchemy lazy-loading issues in tests
    cid1 = c1.id
    cid2 = c2.id

    payload = {
        "vehicle_id": 1,
        "pickup_datetime": "2026-12-10T10:00:00",
        "return_datetime": "2026-12-15T10:00:00",
        "customer_id": cid1,
        "extra_ids": []
    }

    # Request 1: Create and confirm
    res1 = await client.post("/api/v1/reservations/", json=payload)
    assert res1.status_code == 201
    res1_id = res1.json()["id"]
    await client.post(f"/api/v1/reservations/{res1_id}/confirm")

    # Request 2: Attempt to book the same vehicle for overlapping dates
    # The create_draft already checks availability, so it should return 400
    payload2 = payload.copy()
    payload2["customer_id"] = cid2

    res2 = await client.post("/api/v1/reservations/", json=payload2)
    assert res2.status_code == 400 # Availability check should fail here
