"""This file contains the type model for sqlalchemy"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base
from models.association_model import EventType

class Type(Base):
    """type table in db"""
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)

    events = relationship('Event', secondary=EventType, back_populates='types')
