"""This file contains the llike model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.db import Base

class Like(Base):
    """like table in db"""
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    event_id = Column(Integer, ForeignKey("events.id"))
    created_at = Column(DateTime, default=datetime.now())


    profile = relationship("Profile", foreign_keys=[profile_id])
    event = relationship("Event", foreign_keys=[event_id])
