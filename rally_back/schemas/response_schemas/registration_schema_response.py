from datetime import datetime
from pydantic import BaseModel

from schemas.response_schemas.profile_schema_response import ProfileRestrictedSchemaResponse
from enums.payment_status import PaymentStatusEnum

class RegistrationSchemaResponseSchemas(BaseModel):
    """the response schema for registration"""
    id: int
    profile: ProfileRestrictedSchemaResponse
    event_id: int
    event_title: str
    registered_at: datetime
    payment_status: PaymentStatusEnum

    model_config = {
        "from_attributes": True
    }


class RegistrationListSchemaResponseSchemas(BaseModel):
    """the response schema for many registrations"""
    count: int
    total: int
    data: list[RegistrationSchemaResponseSchemas]

    model_config = {
        "from_attributes": True
    }



class RegistrationNumberSchemaResponseSchemas(BaseModel):
    """the response schema for number of registrations"""
    id: int
    number: int

    model_config = {
        "from_attributes": True
    }


class IsUserRegistered(BaseModel):
    """the response to know if a user is registered to an event"""
    registered: bool

    model_config = {
        "from_attributes": True
    }
