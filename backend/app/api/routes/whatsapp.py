from fastapi import APIRouter, Request, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.services.assistant_service import AssistantService
from app.integrations.ai.provider import MockAIProvider
from app.models.assistant import Conversation, Message
from app.models.reservation import Customer
from sqlalchemy.future import select
from app.core.logging import logger
import hmac
import hashlib

router = APIRouter()

async def validate_twilio_signature(request: Request):
    # Twilio signature validation logic
    # In production, this uses X-Twilio-Signature and the Auth Token
    # For demo, we allow if a specific header is present or just return True
    return True

@router.post("/whatsapp")
async def whatsapp_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    validated: bool = Depends(validate_twilio_signature)
):
    form_data = await request.form()
    from_number = form_data.get("From")
    body = form_data.get("Body")

    # 1. Identify Customer
    res = await db.execute(select(Customer).where(Customer.phone == from_number))
    customer = res.scalar_one_or_none()

    if not customer:
        # Create guest customer
        customer = Customer(
            first_name="Guest",
            last_name="User",
            phone=from_number,
            email=f"{from_number}@whatsapp.com"
        )
        db.add(customer)
        await db.commit()
        await db.refresh(customer)

    # 2. Manage Conversation
    res = await db.execute(
        select(Conversation).where(
            (Conversation.customer_id == customer.id) &
            (Conversation.status == "OPEN")
        )
    )
    conversation = res.scalar_one_or_none()

    if not conversation:
        conversation = Conversation(customer_id=customer.id, channel="WHATSAPP")
        db.add(conversation)
        await db.commit()
        await db.refresh(conversation)

    # 3. Process with Assistant
    provider = MockAIProvider()
    service = AssistantService(db, provider)
    response = await service.process_message(
        conversation_id=conversation.id,
        text=body
    )

    # 4. Send Response (Mocked)
    logger.info(f"[WHATSAPP RESPONSE to {from_number}]: {response['response']}")

    return {"status": "success"}
