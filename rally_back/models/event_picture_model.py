"""This file contains the event picture model for sqlalchemy"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class EventPicture(Base):
    """event picture table in db"""
    __tablename__ = "event_pictures"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"))
    photo = Column(String)

    event = relationship("Event", back_populates="pictures")
