from datetime import datetime
from pydantic import BaseModel

from schemas.response_schemas.reason_schema_response import ReasonSchemaResponse
from schemas.response_schemas.event_schema_response import EventSchemaResponse

class SignaledEventSchemaResponse(BaseModel):
    """the response schema for signaled events"""
    id: int
    event: EventSchemaResponse
    reason: ReasonSchemaResponse
    user_id: int
    created_at: datetime
    status: str

    model_config = {
        "from_attributes": True
    }


class SignaledEventListSchemaResponse(BaseModel):
    """the response schema for many registrations"""
    count: int
    data: list[SignaledEventSchemaResponse]

    model_config = {
        "from_attributes": True
    }
