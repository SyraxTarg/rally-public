from pydantic import BaseModel

# pylint: disable=R0801

class CommentSchema(BaseModel):
    """the request schema for comments"""
    event_id: int
    content: str
