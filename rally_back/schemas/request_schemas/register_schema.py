from pydantic import BaseModel

class RegisterSchema(BaseModel):
    """the request schema for user registration"""
    email: str
    password: str
    phone_number: str
    first_name: str
    last_name: str
    photo: str
