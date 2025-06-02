from pydantic import BaseModel

# pylint: disable=R0801

class EventPictureSchema(BaseModel):
    """the request schema for event pictures"""
    photo: str
