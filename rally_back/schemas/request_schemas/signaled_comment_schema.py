from pydantic import BaseModel

class SignaledCommentByCurrentUserSchema(BaseModel):
    """the request schema to signal a comment"""
    comment_id: int
    reason_id: int
