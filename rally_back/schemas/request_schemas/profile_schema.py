from pydantic import BaseModel
from schemas.request_schemas.user_schema import UserSchema

class ProfileSchema(BaseModel):
    """the request schema for profiles"""
    first_name: str
    last_name: str
    photo: str
    nb_like: int
    user: UserSchema


class ModifyProfileSchema(BaseModel):
    """the request to modify a profile"""
    first_name: str
    last_name: str
    photo: str
    phone_number: str
