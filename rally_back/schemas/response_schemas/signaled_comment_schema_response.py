from datetime import datetime
from pydantic import BaseModel

from schemas.response_schemas.reason_schema_response import ReasonSchemaResponse
from schemas.response_schemas.comment_schema_response import CommentSchemaResponse

class SignaledCommentSchemaResponse(BaseModel):
    """the response schema for signaled comment"""
    id: int
    comment: CommentSchemaResponse
    reason: ReasonSchemaResponse
    user_id: int
    created_at: datetime
    status: str

    model_config = {
        "from_attributes": True
    }


class SignaledCommentListSchemaResponse(BaseModel):
    """the response schema for many registrations"""
    count: int
    total: int
    data: list[SignaledCommentSchemaResponse]

    model_config = {
        "from_attributes": True
    }
