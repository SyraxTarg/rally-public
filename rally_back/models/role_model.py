"""This file contains the role model for sqlalchemy"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database.db import Base

class Role(Base):
    """role table in db"""
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String)

    user = relationship("User", back_populates="role")
