from typing import Optional
from sqlalchemy.orm import Session
from fastapi import status

from errors import TypeNotFound
from models.type_model import Type
from repositories import type_repo



def create_type(db: Session, type: str)->Type:
    """used to create a new type"""
    new_type = Type(
        type=type
    )
    type_repo.add_type(db, new_type)
    type_repo.commit_type(db)
    type_repo.refresh_type(db, new_type)
    return new_type

def get_type_by_id(db: Session, type_id: int)->Optional[Type]:
    """used to get a type by its id"""
    type_ = type_repo.get_type_by_id(db, type_id)
    if not type_:
        raise TypeNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Type not found"
        )
    return type_

def get_types(db: Session)->list[Type]:
    """used to get all types"""
    return type_repo.get_types(db)

def get_event_types(db: Session, event_id: int)->list[Type]:
    """used to get types from an event"""
    return type_repo.get_event_types(db, event_id)

def delete_type(db: Session, type_id: int) -> None:
    """used to delete a type by its id"""
    type_ = get_type_by_id(db, type_id)

    if not type_:
        raise TypeNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Type not found"
        )

    type_repo.delete_type(db, type_)
    type_repo.commit_type(db)
