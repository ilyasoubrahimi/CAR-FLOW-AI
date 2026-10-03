from abc import ABC, abstractmethod
from typing import Any, Dict
import httpx
from app.core.logging import logger

class MessagingService(ABC):
    @abstractmethod
    async def send_message(self, recipient: str, content: str, channel: str = "whatsapp") -> bool:
        pass

class TwilioMessagingService(MessagingService):
    def __init__(self, account_sid: str, auth_token: str, from_number: str):
        self.account_sid = account_sid
        self.auth_token = auth_token
        self.from_number = from_number
        self.client = httpx.AsyncClient()

    async def send_message(self, recipient: str, content: str, channel: str = "whatsapp") -> bool:
        # Twilio API implementation
        url = f"https://api.twilio.com/2010-04-01/Accounts/{self.account_sid}/Messages.json"
        data = {
            "From": f"whatsapp:{self.from_number}",
            "To": f"whatsapp:{recipient}",
            "Body": content
        }

        # In a real environment, we use basic auth with account_sid and auth_token
        # For the demo, we'll simulate the call if credentials aren't set
        if self.account_sid == "your_twilio_account_sid":
            logger.info(f"[MOCK] Twilio sending to {recipient}: {content}")
            return True

        try:
            response = await self.client.post(url, data=data, auth=(self.account_sid, self.auth_token))
            return response.status_code == 201
        except Exception as e:
            logger.error(f"Twilio Error: {e}")
            return False
