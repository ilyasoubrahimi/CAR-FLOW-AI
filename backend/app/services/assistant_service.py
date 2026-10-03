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
            # Attempt to extract a category from the text via the provider
            params = await self.provider.extract_parameters(text, {"category": "string"})
            category = params.get("category")
            vehicles = await self._tool_search_vehicles(category=category)
            tools_results["vehicles"] = vehicles
        elif intent == "calculate_quote":
            # In a real flow, we'd extract vehicle_id from context or text
            # For demo, we use the first available vehicle if none specified
            params = await self.provider.extract_parameters(text, {"vehicle_id": "integer"})
            vehicle_id = params.get("vehicle_id", 1)
            quote = await self._tool_calculate_quote(vehicle_id=vehicle_id)
            tools_results["quote"] = quote.model_dump() if hasattr(quote, "model_dump") else quote

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
            "reservation_context": {
                "intent": intent,
                "extracted_params": tools_results
            }
        }

    async def _get_conversation_history(self, conversation_id: int) -> List[Dict[str, str]]:
        result = await self.session.execute(
            select(Message).where(Message.conversation_id == conversation_id).order_by(Message.created_at)
        )
        messages = result.scalars().all()
        return [{"role": m.role, "content": m.content} for m in messages]

    def _get_suggested_actions(self, intent: str) -> List[str]:
        if intent == "search_vehicles":
            return ["Check availability", "Compare cars", "Book now"]
        if intent == "calculate_quote":
            return ["Reserve this car", "Change dates"]
        return ["Start reservation", "Talk to agent"]

    # Tool Implementations
    async def _tool_search_vehicles(self, category: Optional[str] = None):
        repo = VehicleRepository(self.session)
        if category:
            # Use the newly implemented search_vehicles for filtered results
            vehicles = await repo.search_vehicles(category=category)
        else:
            vehicles = await repo.search_vehicles()

        # Convert Vehicle models to dictionaries to avoid Pydantic serialization errors in the response
        return [
            {
                "id": v.id,
                "slug": v.slug,
                "brand": v.brand,
                "model": v.model,
                "year": v.year,
                "category": v.category,
                "transmission": v.transmission,
                "fuel": v.fuel,
                "seats": v.seats,
                "luggage": v.luggage,
                "air_conditioning": v.air_conditioning,
                "description": v.description,
                "short_description": v.short_description,
                "daily_price": float(v.daily_price),
                "status": v.status,
                "featured": v.featured,
            }
            for v in vehicles
        ]

    async def _tool_calculate_quote(self, vehicle_id: int):
        service = PricingService(self.session)
        # Mock dates for demo: today to +3 days
        from datetime import datetime, timedelta
        return await service.calculate_quote(
            vehicle_id,
            datetime.now(),
            datetime.now() + timedelta(days=3)
        )
