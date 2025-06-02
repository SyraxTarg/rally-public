from pydantic import BaseModel

class ReasonSchemaResponse(BaseModel):
    """the response schema for reason"""
    id: int
    reason: str

    model_config = {
        "from_attributes": True
    }

class ReasonListSchemaResponse(BaseModel):
    """the response schema for many reasons"""
    count: int
    data: list[ReasonSchemaResponse]

    model_config = {
        "from_attributes": True
    }
