from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enums.payment_status import PaymentStatusEnum

class PaymentSchemaResponse(BaseModel):
    """the response schema for payment"""
    id: int
    event_id: Optional[int]
    event_title: str
    buyer_id: Optional[int]
    buyer_email: str
    organizer_id: Optional[int]
    organizer_email: str
    amount: float
    fee: float
    brut_amount: float
    stripe_session_id: str
    stripe_payment_intent_id: Optional[str]
    status: PaymentStatusEnum
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class PaymentRestrictedSchemaResponse(BaseModel):
    """the response schema restricted for payment"""
    id: int
    event_id: int
    event_title: str
    buyer_id: int
    buyer_email: str
    organizer_id: int
    organizer_email: str
    brut_amount: float
    status: PaymentStatusEnum
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class PaymentListSchemaResponse(BaseModel):
    """the response schema for many payments"""
    count: int
    data: list[PaymentSchemaResponse]
    total: int

    model_config = {
        "from_attributes": True
    }

class PaymentRestrictedListSchemaResponse(BaseModel):
    """the response schema for many payments restricted"""
    count: int
    data: list[PaymentRestrictedSchemaResponse]

    model_config = {
        "from_attributes": True
    }
