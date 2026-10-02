from typing import List, Dict, Any, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.integrations.ai.provider import AIProvider, MockAIProvider
from app.integrations.ai.tools import tool_registry
from app.services.availability_service import AvailabilityService
from app.services.pricing_service import PricingService
from app.services.reservation_service import ReservationService
from app.repositories.vehicle import VehicleRepository
from app.models.assistant import Conversation, Message

class AssistantService:
    def __init__(self, session: AsyncSession, provider: AIProvider):
        self.session = session
        self.provider = provider

    async def process_message(self, conversation_id: int, text: str, language: str = "fr") -> Dict[str, Any]:
        # 1. Store incoming message
        message = Message(conversation_id=conversation_id, role="USER", content=text)
        self.session.add(message)
        await self.session.flush()

        # 2. Extract Intent and Parameters
        intent_data = await self.provider.extract_intent(text)
        intent = intent_data.get("intent")

        # 3. Tool Execution Loop
        tools_results = {}
        if intent == "search_vehicles":
            # Mocking parameter extraction for the demo
            vehicles = await self._tool_search_vehicles(category=None)
            tools_results["vehicles"] = vehicles
        elif intent == "calculate_quote":
            # Mocking parameters
            quote = await self._tool_calculate_quote(vehicle_id=1)
            tools_results["quote"] = quote

        # 4. Generate Response
        history = await self._get_conversation_history(conversation_id)
        response_text = await self.provider.generate_response(
            prompt=text,
            history=history,
            tools_results=tools_results
        )

        # 5. Store AI response
        ai_msg = Message(conversation_id=conversation_id, role="ASSISTANT", content=response_text)
        self.session.add(ai_msg)
        await self.session.commit()

        return {
            "conversation_id": conversation_id,
            "response": response_text,
            "suggested_actions": self._get_suggested_actions(intent),
            "reservation_context": {}
        }

    async def _get_conversation_history(self, conversation_id: int) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        )
        messages = result.scalars().all()
        return [{"role": m.role, "content": m.content} for m in messages]

    def _get_suggested_actions(self, intent: str) -> List[str]:
        if intent == "search_vehicles":
            return ["Check availability", "Compare cars"]
        return ["Start reservation", "Talk to agent"]

    # Tool Implementations
    async def _tool_search_vehicles(self, category: Optional[str] = None):
        repo = VehicleRepository(self.session)
        return await repo.get_all()

    async def _tool_calculate_quote(self, vehicle_id: int):
        service = PricingService(self.session)
        # Mock dates for demo
        from datetime import datetime, timedelta
        return await service.calculate_quote(
            vehicle_id,
            datetime.now(),
            datetime.now() + timedelta(days=3)
        )
