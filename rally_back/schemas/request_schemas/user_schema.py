from pydantic import BaseModel

class UserAuth(BaseModel):
    """the request schema for authentication"""
    email: str
    password: str

class UserSchema(BaseModel):
    """the request schema for user"""
    email: str
    phone_number: str
    is_planner: bool
