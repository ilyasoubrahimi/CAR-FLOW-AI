from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from decimal import Decimal
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

class PaymentStatus(Enum):
    UNPAID = "UNPAID"
    PENDING = "PENDING"
    PARTIALLY_PAID = "PARTIALLY_PAID"
    PAID = "PAID"
    REFUNDED = "REFUNDED"

class PaymentRequest(BaseModel):
    reservation_id: int
    amount: Decimal
    payment_method: str
    currency: str = "MAD"

class PaymentResponse(BaseModel):
    transaction_id: str
    status: PaymentStatus
    amount_paid: Decimal
    timestamp: datetime

class PaymentService(ABC):
    @abstractmethod
    async def create_payment_intent(self, request: PaymentRequest) -> str:
        """Returns a client secret or payment URL"""
        pass

    @abstractmethod
    async def confirm_payment(self, transaction_id: str) -> PaymentResponse:
        pass

    @abstractmethod
    async def refund_payment(self, transaction_id: str) -> bool:
        pass

class MockPaymentService(PaymentService):
    async def create_payment_intent(self, request: PaymentRequest) -> str:
        return "mock_payment_intent_secret_12345"

    async def confirm_payment(self, transaction_id: str) -> PaymentResponse:
        return PaymentResponse(
            transaction_id=transaction_id,
            status=PaymentStatus.PAID,
            amount_paid=Decimal(0), # In reality, fetch from intent
            timestamp=datetime.now()
        )

    async def refund_payment(self, transaction_id: str) -> bool:
        return True
