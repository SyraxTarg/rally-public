from pydantic import BaseModel

# pylint: disable=R0801

class AddressSchema(BaseModel):
    """the request schema for addresses"""
    city: str
    zipcode: str
    number: str
    street: str
    country: str
