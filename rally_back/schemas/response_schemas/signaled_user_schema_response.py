from datetime import datetime
from pydantic import BaseModel

from schemas.response_schemas.reason_schema_response import ReasonSchemaResponse

class SignaledUserSchemaResponse(BaseModel):
    """the response schema for signaled user"""
    id: int
    user_signaled_id: int
    user_signaled_email: str
    reason: ReasonSchemaResponse
    signaled_by_id: int
    signaled_by_email: str
    created_at: datetime
    status: str

    model_config = {
        "from_attributes": True
    }


class SignaledUserListSchemaResponse(BaseModel):
    """the response schema for many signaled users"""
    count: int
    total: int
    data: list[SignaledUserSchemaResponse]

    model_config = {
        "from_attributes": True
    }
