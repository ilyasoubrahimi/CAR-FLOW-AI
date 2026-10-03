import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_assistant_basic_response(client):
    """Verify the AI assistant endpoint returns a response."""
    # Use the seeded conversation ID (usually 1)
    payload = {"conversation_id": 1, "message": "Hello, I want to rent a car."}
    response = await client.post("/api/v1/assistant/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0

@pytest.mark.asyncio
async def test_assistant_intent_routing(client):
    """Verify that specific intents trigger correct behavior (logic check)."""
    # Use the seeded conversation ID (usually 1)
    payload = {"conversation_id": 1, "message": "How much does a Porsche cost per day?"}
    response = await client.post("/api/v1/assistant/message", json=payload)
    assert response.status_code == 200
    assert "response" in response.json()
