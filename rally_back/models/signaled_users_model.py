"""This file contains the signaled users model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class SignaledUser(Base):
    """signaled users table in db"""
    __tablename__ = "signaled_users"

    id = Column(Integer, primary_key=True, index=True)
    user_signaled_id = Column(Integer, ForeignKey("users.id"))
    reason_id = Column(Integer, ForeignKey("reasons.id"))
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")

    user_signaled = relationship("User", foreign_keys=[user_signaled_id])
    user = relationship("User", foreign_keys=[user_id])
    reason = relationship("Reason", back_populates="signaled_users")
