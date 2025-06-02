from pydantic import BaseModel

class AddressSchemaResponse(BaseModel):
    """the response schema for address"""
    id: int
    city: str
    zipcode: str
    number: str
    street: str
    country: str

    model_config = {
        "from_attributes": True
    }
