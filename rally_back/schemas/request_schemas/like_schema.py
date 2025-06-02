from pydantic import BaseModel

class LikeSchema(BaseModel):
    """the request schema for likes"""
    profile_id: int
    event_id: int
