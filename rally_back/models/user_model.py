"""This file contains the user model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.db import Base

class User(Base):
    """user table in db"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    phone_number = Column(String)
    is_planner = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.now())
    role_id = Column(Integer, ForeignKey("roles.id"))
    account_id = Column(String, nullable=True)
    is_verified = Column(Boolean, default=False)
    verification_token = Column(Integer, nullable=True, default=None)
    verification_token_sent_at = Column(DateTime, nullable=True, default=None)

    role = relationship("Role", back_populates="user", uselist=False)
    profile = relationship("Profile", back_populates="user", cascade="all, delete-orphan", uselist=False)
