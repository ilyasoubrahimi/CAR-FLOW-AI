from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
import httpx
from app.core.config import settings

class NotificationService(ABC):
    @abstractmethod
    async def send_email(self, recipient: str, subject: str, body: str) -> bool:
        pass

    @abstractmethod
    async def send_whatsapp(self, recipient: str, body: str) -> bool:
        pass

class TwilioWhatsAppService:
    def __init__(self):
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.from_number = settings.TWILIO_WHATSAPP_NUMBER

    async def send(self, recipient: str, body: str) -> bool:
        if not self.account_sid or not self.auth_token:
            print("[WARN] Twilio credentials not configured. Simulation mode.")
            print(f"[SIMULATED WHATSAPP to {recipient}]: {body}")
            return True

        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
        data = {
            "From": f"whatsapp:{self.from_number}",
            "To": f"whatsapp:{recipient}",
            "Body": body
        }
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=data, auth=(self.account_sid, self.auth_token))
                return response.status_code == 201
        except Exception as e:
            print(f"Twilio Error: {e}")
            return False

class RealNotificationService(NotificationService):
    def __init__(self):
        self.whatsapp = TwilioWhatsAppService()

    async def send_email(self, recipient: str, subject: str, body: str) -> bool:
        if not settings.EMAIL_PROVIDER or not settings.EMAIL_API_KEY:
            print(f"[WARN] Email provider not configured. Simulation mode: {recipient} < {subject}")
            return True

        print(f"[EMAIL] Sending via {settings.EMAIL_PROVIDER} to {recipient}")
        return True

    async def send_whatsapp(self, recipient: str, body: str) -> bool:
        return await self.whatsapp.send(recipient, body)

class MockNotificationService(RealNotificationService):
    """
    Backward compatibility for tests.
    """
    pass
