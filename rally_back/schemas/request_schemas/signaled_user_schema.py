from pydantic import BaseModel

class SignaledUserCurrentUSerSchema(BaseModel):
    """the request schema to signal a user"""
    user_signaled_id: int
    reason_id: int
