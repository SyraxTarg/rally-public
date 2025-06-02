from datetime import datetime
from pydantic import BaseModel

class BannedUserSchemaResponse(BaseModel):
    """the response schema for banned user"""
    id: int
    banned_email: str
    banned_by_email: str
    banned_at: datetime

    model_config = {
        "from_attributes": True
    }

class BannedUserListSchemaResponse(BaseModel):
    """the response schema for many banned users"""
    count: int
    data: list[BannedUserSchemaResponse]

    model_config = {
        "from_attributes": True
    }
