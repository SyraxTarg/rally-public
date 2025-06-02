from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum
from schemas.response_schemas.user_schema_response import UserResponse

class ActionLogSchemaResponse(BaseModel):
    """the response schema for action log"""
    id: int
    logLevel: LogLevelEnum
    user: Optional[UserResponse]
    actionType: ActionEnum
    description: str
    date: datetime

    model_config = {
        "from_attributes": True
    }

class ActionLogListResponse(BaseModel):
    """the response schema for many action log"""
    count: int
    total: int
    data: list[ActionLogSchemaResponse]

    model_config = {
        "from_attributes": True
    }
