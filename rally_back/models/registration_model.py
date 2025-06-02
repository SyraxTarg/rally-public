"""This file contains the registration model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from database.db import Base
from enums.payment_status import PaymentStatusEnum

class Registration(Base):
    """registration table in db"""
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    registered_at = Column(DateTime, default=datetime.now())
    payment_status = Column(String, default=PaymentStatusEnum.PENDING)


    profile = relationship("Profile", foreign_keys=[profile_id])
    event = relationship("Event", foreign_keys=[event_id])
