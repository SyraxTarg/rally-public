from pydantic import BaseModel

class TypeSchemaResponse(BaseModel):
    """the response schema for type"""
    id: int
    type: str

    model_config = {
        "from_attributes": True
    }


class TypeListSchemaResponse(BaseModel):
    """the response schema for many types"""
    count: int
    data: list[TypeSchemaResponse]

    model_config = {
        "from_attributes": True
    }
