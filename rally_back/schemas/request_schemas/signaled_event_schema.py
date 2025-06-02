from pydantic import BaseModel

class SignaledEventByCurrentUserSchema(BaseModel):
    """the request schema to signal an event"""
    event_id: int
    reason_id: int
