from pydantic import BaseModel

class RegisterSchemaResponse(BaseModel):
    """the response schema for user register"""
    email: str
    password: str
    phone_number: str
    first_name: str
    last_name: str

    model_config = {
        "from_attributes": True
    }
