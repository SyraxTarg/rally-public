"""This file contains the signaled events model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class SignaledEvent(Base):
    """signaled events table in db"""
    __tablename__ = "signaled_events"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    reason_id = Column(Integer, ForeignKey("reasons.id"))
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")

    event = relationship("Event", foreign_keys=[event_id])
    user = relationship("User", foreign_keys=[user_id])
    reason = relationship("Reason", back_populates="signaled_events")
