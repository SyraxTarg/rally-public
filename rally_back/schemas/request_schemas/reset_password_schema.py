from pydantic import BaseModel

class ResetPasswordSchema(BaseModel):
    """the schema request for password modification"""
    token: str
    new_password: str
    confirm_password: str
