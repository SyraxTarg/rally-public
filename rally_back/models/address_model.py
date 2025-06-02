"""This file contains the address model for sqlalchemy"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database.db import Base

class Address(Base):
    """Address model that will be used as a table in db"""
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    city = Column(String)
    zipcode = Column(String)
    number = Column(String)
    street = Column(String)
    country = Column(String)

    event = relationship("Event", back_populates="address", uselist=False, cascade="all, delete-orphan", single_parent=True)
