from datetime import datetime
from pydantic import BaseModel

from schemas.response_schemas.user_schema_response import UserResponse

class ProfileSchemaResponse(BaseModel):
    """the response schema for profile"""
    id: int
    first_name: str
    last_name: str
    photo: str
    nb_like: int
    user: UserResponse
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }

class ProfileRestrictedSchemaResponse(BaseModel):
    """the response schema for profile restricted"""
    id: int
    first_name: str
    last_name: str
    photo: str
    nb_like: int
    email: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class ProfileListSchemaResponse(BaseModel):
    """the response schema for many profiles"""
    count: int
    total: int
    data: list[ProfileSchemaResponse]

    model_config = {
        "from_attributes": True
    }

class ProfileRestrictedListSchemaResponse(BaseModel):
    """the response schema for many payments restricted"""
    count: int
    data: list[ProfileRestrictedSchemaResponse]

    model_config = {
        "from_attributes": True
    }
