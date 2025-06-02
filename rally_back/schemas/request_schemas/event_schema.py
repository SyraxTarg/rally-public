from datetime import datetime
from pydantic import BaseModel
from schemas.request_schemas.type_schema import TypesIdsSchema
from schemas.request_schemas.address_schema import AddressSchema
from schemas.request_schemas.event_picture_schema import EventPictureSchema

# pylint: disable=R0801

class EventSchema(BaseModel):
    """the request schema for events"""
    title: str
    description: str
    nb_places: int
    price: float
    date: datetime
    cloture_billets: datetime
    types: TypesIdsSchema
    address: AddressSchema
    pictures: list[EventPictureSchema]
