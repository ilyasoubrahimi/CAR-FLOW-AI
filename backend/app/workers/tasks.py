from app.workers.celery_app import celery_app
from app.integrations.twilio.service import TwilioMessagingService
from app.core.config import settings
import asyncio

# Utility to run async code in sync Celery tasks
def run_async(coro):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(coro)

@celery_app.task(name="send_confirmation_message")
def send_confirmation_message(reservation_id: int, phone: str, message: str):
    # In reality, we'd initialize the service with settings
    service = TwilioMessagingService(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
        settings.TWILIO_WHATSAPP_NUMBER
    )
    return run_async(service.send_message(recipient=phone, content=message))

@celery_app.task(name="send_reminder_message")
def send_reminder_message(phone: str, message: str):
    service = TwilioMessagingService(
        settings.TWILIO_ACCOUNT_SID,
        settings.TWILIO_AUTH_TOKEN,
        settings.TWILIO_WHATSAPP_NUMBER
    )
    return run_async(service.send_message(recipient=phone, content=message))

@celery_app.task(name="process_abandoned_reservation")
def process_abandoned_reservation(reservation_id: int, phone: str):
    # Check if still DRAFT and not confirmed
    # If so, send "Still interested?" message
    message = "Vous étiez en train de réserver un véhicule. Souhaitez-vous finaliser votre réservation ?"
    return send_reminder_message.delay(phone, message)
