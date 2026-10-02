from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.services.assistant_service import AssistantService
from app.integrations.ai.provider import MockAIProvider
from app.schemas.assistant import AssistantRequest, AssistantResponse

router = APIRouter()

@router.post("/message", response_model=AssistantResponse)
async def chat_with_assistant(
    request: AssistantRequest,
    db: AsyncSession = Depends(get_db)
):
    # In production, we'd resolve the provider from config (e.g. OpenAIProvider)
    provider = MockAIProvider()
    service = AssistantService(db, provider)

    return await service.process_message(
        conversation_id=request.conversation_id,
        text=request.message,
        language=request.language
    )
