"""This file contains the type repository"""
from typing import Optional
from sqlalchemy.orm import Session

from models.type_model import Type
from models.association_model import EventType

def add_type(db: Session, type_: Type) -> None:
    """Add a new type to the database."""
    db.add(type_)

def commit_type(db: Session) -> None:
    """Commit the current transaction related to types."""
    db.commit()

def refresh_type(db: Session, type_: Type) -> None:
    """Refresh the state of a type from the database."""
    db.refresh(type_)

def get_type_by_id(db: Session, type_id: int) -> Optional[Type]:
    """Retrieve a type by its ID."""
    return db.query(Type).filter(Type.id == type_id).first()

def get_types(db: Session) -> None:
    """Retrieve all types from the database."""
    return db.query(Type).all()

def get_event_types(db: Session, event_id: int) -> list[Type]:
    """Retrieve types associated with a specific event by event ID."""
    return (
        db.query(Type)
        .join(EventType, Type.id == EventType.c.type_id)
        .filter(EventType.c.event_id == event_id)
        .all()
    )

def delete_type(db: Session, type_: Type) -> None:
    """Delete a type from the database."""
    db.delete(type_)
