"""This file contains the comment model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from database.db import Base

class Comment(Base):
    """comment table in db"""
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    created_at = Column(DateTime, default=datetime.now())


    profile = relationship("Profile", foreign_keys=[profile_id])
    event = relationship("Event", foreign_keys=[event_id])
