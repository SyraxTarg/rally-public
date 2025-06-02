"""This file contains the association models for sqlalchemy"""
from sqlalchemy import Column, Integer, ForeignKey, Table
from database.db import Base

EventType = Table(
    "event_type",
    Base.metadata,
    Column("event_id", Integer, ForeignKey("events.id"), primary_key=True),
    Column("type_id", Integer, ForeignKey("types.id"), primary_key=True),
)
