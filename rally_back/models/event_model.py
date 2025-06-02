"""This file contains the event model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Double, Text
from sqlalchemy.orm import relationship
from models.association_model import EventType
from database.db import Base

class Event(Base):
    """event table in db"""
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    nb_places = Column(Integer)
    price = Column(Double)
    profile_id = Column(Integer, ForeignKey("profiles.id"))
    nb_likes = Column(Integer)
    nb_comments = Column(Integer)
    date = Column(DateTime)
    cloture_billets = Column(DateTime)
    address_id = Column(Integer, ForeignKey("addresses.id"))
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now())


    profile = relationship("Profile", foreign_keys=[profile_id])
    types = relationship("Type", secondary=EventType, back_populates="events")
    address = relationship("Address", back_populates="event", uselist=False, single_parent=True)
    pictures = relationship("EventPicture", back_populates="event", cascade="all, delete-orphan")
