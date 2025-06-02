"""This file contains the signaled comments model for sqlalchemy"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base

class SignaledComment(Base):
    """signaled comments table in db"""
    __tablename__ = "signaled_comments"

    id = Column(Integer, primary_key=True, index=True)
    comment_id = Column(Integer, ForeignKey("comments.id"))
    reason_id = Column(Integer, ForeignKey("reasons.id"))
    created_at = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")

    comment_signaled = relationship("Comment", foreign_keys=[comment_id])
    user = relationship("User", foreign_keys=[user_id])
    reason = relationship("Reason", back_populates="signaled_comments")
