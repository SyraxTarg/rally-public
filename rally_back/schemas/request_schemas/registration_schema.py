from pydantic import BaseModel

class RegistrationSchema(BaseModel):
    """the request schema for registration"""
    event_id: int
