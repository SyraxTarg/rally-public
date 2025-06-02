"""This file contains the failed login model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database.db import Base

class FailedLogin(Base):
    """failed login table in db"""
    __tablename__ = "failed_logins"

    id = Column(Integer, primary_key=True, index=True)
    ip_address = Column(String, unique=True, index=True)
    attempts = Column(Integer, default=0)
    last_attempt = Column(DateTime, default=datetime.now())
