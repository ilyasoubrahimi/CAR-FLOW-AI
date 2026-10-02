from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class AssistantRequest(BaseModel):
    conversation_id: int
    message: str
    language: str = "fr"

class AssistantResponse(BaseModel):
    conversation_id: int
    response: str
    suggested_actions: List[str]
    reservation_context: Dict[str, Any]
