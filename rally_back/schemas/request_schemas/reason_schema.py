from pydantic import BaseModel

class ReasonSchema(BaseModel):
    """the request schema for reasons"""
    reason: str
