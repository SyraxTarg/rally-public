"""This file contains the reason model for sqlalchemy"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base

class Reason(Base):
    """reason table in db"""
    __tablename__ = "reasons"

    id = Column(Integer, primary_key=True, index=True)
    reason = Column(String, nullable=False, unique=True)

    signaled_users = relationship("SignaledUser", back_populates="reason")
    signaled_comments = relationship("SignaledComment", back_populates="reason")
    signaled_events = relationship("SignaledEvent", back_populates="reason")
