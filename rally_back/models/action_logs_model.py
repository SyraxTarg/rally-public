"""This file contains the action log model for sqlalchemy"""
from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime, Enum
from sqlalchemy.orm import relationship
from database.db import Base
from enums import action, log_level

class ActionLog(Base):
    """Action log model that will be translated as a table in db"""
    __tablename__ = "action_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    log_type = Column(Enum(log_level.LogLevelEnum))
    action_type = Column(Enum(action.ActionEnum))
    description = Column(Text)
    date = Column(DateTime)

    user = relationship("User", foreign_keys=[user_id])
