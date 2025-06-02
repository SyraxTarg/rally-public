from pydantic import BaseModel

class TypeSchema(BaseModel):
    """the request schema for a type"""
    type: str

class TypesIdsSchema(BaseModel):
    """the request schema for many types"""
    types: list[int]
