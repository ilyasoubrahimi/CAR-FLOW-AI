from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class AIProvider(ABC):
    @abstractmethod
    async def generate_response(self, prompt: str, history: List[Dict[str, str]], tools_results: Optional[Dict[str, Any]] = None) -> str:
        pass

    @abstractmethod
    async def extract_intent(self, text: str) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def extract_parameters(self, text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        pass

class MockAIProvider(AIProvider):
    """Development provider that simulates AI behavior without requiring API keys."""
    async def generate_response(self, prompt: str, history: List[Dict[str, str]], tools_results: Optional[Dict[str, Any]] = None) -> str:
        if tools_results and "vehicles" in tools_results:
            vehicles = tools_results["vehicles"]
            if vehicles:
                return f"I found {len(vehicles)} cars matching your needs. The best option is {vehicles[0].brand} {vehicles[0].model}."
            return "I couldn't find any cars matching those criteria."

        if "hello" in prompt.lower():
            return "Hello! I'm the Marrakech Drive assistant. How can I help you find your perfect car?"

        return "I understand. Let me check that for you. Could you please provide your pickup date?"

    async def extract_intent(self, text: str) -> Dict[str, Any]:
        text = text.lower()
        if any(word in text for word in ["rent", "book", "find", "search", "voiture", "car"]):
            return {"intent": "search_vehicles", "confidence": 0.9}
        if any(word in text for word in ["price", "cost", "combien", "prix"]):
            return {"intent": "calculate_quote", "confidence": 0.9}
        return {"intent": "general_query", "confidence": 0.5}

    async def extract_parameters(self, text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        # Simplified mock extraction
        return {}
