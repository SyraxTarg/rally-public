"""This file contains the banned users model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base

class BannedUser(Base):
    """banned users table in db"""
    __tablename__ = "banned_users"

    id = Column(Integer, primary_key=True, index=True)
    banned_email = Column(String, nullable=False, unique=True)
    banned_by_email = Column(String, nullable=True)
    banned_at = Column(DateTime, default=datetime.now())
