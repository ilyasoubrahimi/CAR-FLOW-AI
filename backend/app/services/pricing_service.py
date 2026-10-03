from decimal import Decimal
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from app.models.reservation import PricingRule, Extra
from app.models.vehicle import Vehicle

class PricingBreakdown(BaseModel):
    subtotal: Decimal
    discount: Decimal
    extras_total: Decimal
    delivery_fee: Decimal
    total: Decimal
    currency: str

class PricingService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def calculate_quote(self, vehicle_id: int, pickup_datetime: datetime, return_datetime: datetime, extra_ids: List[int] = None) -> PricingBreakdown:
        # 1. Get Vehicle and Base Price
        result = await self.session.execute(select(Vehicle).where(Vehicle.id == vehicle_id))
        vehicle = result.scalar_one_or_none()
        if not vehicle:
            raise ValueError("Vehicle not found")

        # 2. Calculate Duration
        duration = (return_datetime - pickup_datetime).days
        if duration <= 0:
            duration = 1 # Minimum 1 day

        # 3. Apply Duration-based Pricing Rules
        base_daily_price = vehicle.daily_price

        # Fetch relevant pricing rules
        rules_query = select(PricingRule).where(
            (PricingRule.vehicle_id == vehicle_id) | (PricingRule.vehicle_id == None),
            PricingRule.active == True
        )
        rules_result = await self.session.execute(rules_query)
        rules = rules_result.scalars().all()

        # Apply rule based on duration
        # In a real system, we'd pick the most specific rule.
        for rule in rules:
            if rule.min_days <= duration and (rule.max_days is None or duration <= rule.max_days):
                if rule.modifier_type == "PERCENTAGE":
                    base_daily_price *= rule.price_modifier
                elif rule.modifier_type == "FIXED":
                    base_daily_price += rule.price_modifier
                break # Use first matching rule

        subtotal = Decimal(base_daily_price) * duration

        # 4. Calculate Extras
        extras_total = Decimal(0)
        if extra_ids:
            extras_query = select(Extra).where(Extra.id.in_(extra_ids), Extra.active == True)
            extras_result = await self.session.execute(extras_query)
            extras = extras_result.scalars().all()

            for extra in extras:
                if extra.price_type == "PER_DAY":
                    extras_total += Decimal(extra.price) * duration
                elif extra.price_type == "PER_RENTAL" or extra.price_type == "FIXED":
                    extras_total += Decimal(extra.price)

        # 5. Final Calculation
        delivery_fee = Decimal(0) # Implement based on location_id logic later
        discount = Decimal(0)

        total = subtotal + extras_total + delivery_fee - discount

        return PricingBreakdown(
            subtotal=subtotal,
            discount=discount,
            extras_total=extras_total,
            delivery_fee=delivery_fee,
            total=total,
            currency="MAD"
        )
