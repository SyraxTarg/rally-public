from typing import Optional
from pydantic import BaseModel

from schemas.response_schemas.role_schema_response import RoleSchemaResponse

class UserResponse(BaseModel):
    """the response schema for user"""
    id: int
    email: str
    phone_number: str
    is_planner: bool
    role: RoleSchemaResponse
    account_id: Optional[str]

    model_config = {
        "from_attributes": True
    }


class UserListResponse(BaseModel):
    """the response schema for many users"""
    count: int
    data: list[UserResponse]

    model_config = {
        "from_attributes": True
    }
