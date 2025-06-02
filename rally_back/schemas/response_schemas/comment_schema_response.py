from datetime import datetime
from pydantic import BaseModel

from schemas.response_schemas.profile_schema_response import ProfileRestrictedSchemaResponse

class CommentSchemaResponse(BaseModel):
    """the response schema for comment"""
    id: int
    profile: ProfileRestrictedSchemaResponse
    event_id: int
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class CommentListSchemaResponse(BaseModel):
    """the response schema for many comments"""
    count: int
    data: list[CommentSchemaResponse]

    model_config = {
        "from_attributes": True
    }
