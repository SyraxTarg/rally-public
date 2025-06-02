from pydantic import BaseModel

from schemas.response_schemas.profile_schema_response import ProfileRestrictedSchemaResponse

class LikeSchemaresponseSchemas(BaseModel):
    """the response schema for like"""
    id: int
    profile: ProfileRestrictedSchemaResponse
    event_id: int

    model_config = {
        "from_attributes": True
    }

class IsLikedResponseSchema(BaseModel):
    """the response to know if the event is liked by the user"""
    is_liked: bool

    model_config = {
        "from_attributes": True
    }


class  LikeListSchemaresponseSchemas(BaseModel):
    """the response schema for many likes"""
    count: int
    data: list[LikeSchemaresponseSchemas]

    model_config = {
        "from_attributes": True
    }
