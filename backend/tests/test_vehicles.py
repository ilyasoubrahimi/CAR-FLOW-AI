import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_search_vehicles_basic(client):
    """Verify that we can search for available vehicles."""
    response = await client.get("/api/v1/vehicles/")
    assert response.status_code == 200
    data = response.json()
    assert "vehicles" in data
    assert len(data["vehicles"]) > 0
    assert data["vehicles"][0]["status"] == "AVAILABLE"

@pytest.mark.asyncio
async def test_search_vehicles_filter_category(client):
    """Verify filtering by category."""
    response = await client.get("/api/v1/vehicles/?category=Luxury")
    assert response.status_code == 200
    vehicles = response.json()["vehicles"]
    for v in vehicles:
        assert v["category"] == "Luxury"

@pytest.mark.asyncio
async def test_vehicle_not_found(client):
    """Verify 404 for non-existent vehicle slug."""
    response = await client.get("/api/v1/vehicles/non-existent-slug")
    assert response.status_code == 404
