import httpx
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from app.core.config import settings

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

class OpenAIProvider(AIProvider):
    """Live OpenAI provider using the configured API key and model."""
    def __init__(self):
        self.api_key = settings.AI_API_KEY
        self.model = settings.AI_MODEL or "gpt-4o"
        self.api_url = "https://api.openai.com/v1/chat/completions"

    async def _call_llm(self, messages: List[Dict[str, str]]) -> str:
        if not self.api_key:
            raise ValueError("AI_API_KEY is not configured")

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": 0.7
                },
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()["choices"][0]["message"]["content"]

    async def generate_response(self, prompt: str, history: List[Dict[str, str]], tools_results: Optional[Dict[str, Any]] = None) -> str:
        messages = [{"role": "system", "content": "You are the luxury AI concierge for Marrakech Drive. Be elegant, helpful, and concise."}]
        messages.extend(history)

        if tools_results:
            messages.append({"role": "system", "content": f"Context from system tools: {json.dumps(tools_results)}"})

        messages.append({"role": "user", "content": prompt})
        return await self._call_llm(messages)

    async def extract_intent(self, text: str) -> Dict[str, Any]:
        prompt = f"Analyze the user text and return ONLY a JSON object with 'intent' and 'confidence'. Intents: search_vehicles, calculate_quote, general_query. Text: {text}"
        messages = [{"role": "user", "content": prompt}]
        response = await self._call_llm(messages)
        try:
            return json.loads(response)
        except:
            return {"intent": "general_query", "confidence": 0.5}

    async def extract_parameters(self, text: str, schema: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"Extract parameters from the text based on this schema: {json.dumps(schema)}. Return ONLY a JSON object. Text: {text}"
        messages = [{"role": "user", "content": prompt}]
        response = await self._call_llm(messages)
        try:
            return json.loads(response)
        except:
            return {}

class MockAIProvider(AIProvider):
    """Development provider that simulates AI behavior without requiring API keys."""
    async def generate_response(self, prompt: str, history: List[Dict[str, str]], tools_results: Optional[Dict[str, Any]] = None) -> str:
        if tools_results and "vehicles" in tools_results:
            vehicles = tools_results["vehicles"]
            if vehicles:
                v = vehicles[0]
                brand = v.get("brand") if isinstance(v, dict) else getattr(v, "brand", "Unknown")
                model = v.get("model") if isinstance(v, dict) else getattr(v, "model", "Unknown")
                return f"I found {len(vehicles)} cars matching your needs. The best option is {brand} {model}."
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
        return {}

def get_ai_provider() -> AIProvider:
    """Factory to return the appropriate AI provider based on configuration."""
    if settings.AI_API_KEY:
        return OpenAIProvider()
    return MockAIProvider()
