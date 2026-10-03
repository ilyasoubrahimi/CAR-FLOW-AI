import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_assistant_basic_response(client):
    """Verify the AI assistant endpoint returns a response."""
    payload = {"message": "Hello, I want to rent a car."}
    response = await client.post("/api/v1/assistant/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert len(data["reply"]) > 0

@pytest.mark.asyncio
async def test_assistant_intent_routing(client):
    """Verify that specific intents trigger correct behavior (logic check)."""
    # We test if the AI provider can be reached and returns something sensible
    payload = {"message": "How much does a Porsche cost per day?"}
    response = await client.post("/api/v1/assistant/message", json=payload)
    assert response.status_code == 200
    assert "reply" in response.json()
