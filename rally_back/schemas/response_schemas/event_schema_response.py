from datetime import datetime
from pydantic import BaseModel

from schemas.response_schemas.profile_schema_response import ProfileRestrictedSchemaResponse
from schemas.response_schemas.type_schema_response import TypeSchemaResponse
from schemas.response_schemas.address_schema_response import AddressSchemaResponse
from schemas.response_schemas.event_picture_schema_response import EventPictureSchemaResponse

class EventSchemaResponse(BaseModel):
    """the response schema for event"""
    id: int
    title: str
    description: str
    nb_places: int
    price: float
    profile: ProfileRestrictedSchemaResponse
    nb_likes: int
    nb_comments: int
    date: datetime
    cloture_billets: datetime
    created_at: datetime
    updated_at: datetime
    types: list[TypeSchemaResponse]
    address: AddressSchemaResponse
    pictures: list[EventPictureSchemaResponse]

    model_config = {
        "from_attributes": True
    }


class EventListSchemaResponse(BaseModel):
    """the response schema for many events"""
    count: int
    total: int
    data: list[EventSchemaResponse]

    model_config = {
        "from_attributes": True
    }
