from pydantic import BaseModel

class EventPictureSchemaResponse(BaseModel):
    """the response schema for event picture"""
    id: int
    photo: str

    model_config = {
        "from_attributes": True
    }

class EventPictureListSchemaResponse(BaseModel):
    """the response schema for many event picture"""
    count: int
    data: list[EventPictureSchemaResponse]

    model_config = {
        "from_attributes": True
    }
