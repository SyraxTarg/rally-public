"""This file contains the payment model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Double
from sqlalchemy.orm import relationship
from database.db import Base
from enums.payment_status import PaymentStatusEnum

class Payment(Base):
    """payment model in db"""
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="SET NULL"), nullable=True)
    event_title = Column(String, nullable=False)
    buyer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    buyer_email = Column(String, nullable=False)
    organizer_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    organizer_email = Column(String, nullable=False)
    amount = Column(Double)
    fee = Column(Double)
    brut_amount = Column(Double)
    stripe_session_id = Column(String)
    stripe_payment_intent_id = Column(String, nullable=True)
    status = Column(String, default=PaymentStatusEnum.PENDING)
    created_at = Column(DateTime, default=datetime.now())

    buyer = relationship("User", foreign_keys=[buyer_id])
    organizer = relationship("User", foreign_keys=[organizer_id])
