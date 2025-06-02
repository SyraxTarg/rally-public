from pydantic import BaseModel

class RoleSchemaResponse(BaseModel):
    """the response schema for role"""
    id: int
    role: str

    model_config = {
        "from_attributes": True
    }

class RoleListSchemaResponse(BaseModel):
    """the response schema for many roles"""
    count: int
    data: list[RoleSchemaResponse]

    model_config = {
        "from_attributes": True
    }
