"""This file contains the user repository"""
from typing import Optional
from sqlalchemy.orm import Session

from models.user_model import User

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Retrieve a user by their ID."""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Retrieve a user by their email address."""
    return db.query(User).filter(User.email == email).first()

def add_user(db: Session, user: User) -> None:
    """Add a new user to the database."""
    db.add(user)

def commit_user(db: Session) -> None:
    """Commit the current transaction related to users."""
    db.commit()

def refresh_user(db: Session, user: User) -> None:
    """Refresh the state of a user from the database."""
    db.refresh(user)

def delete_user(db: Session, user: User) -> None:
    """Delete a user from the database."""
    db.delete(user)

def search_users(db: Session, search: Optional[str], offset: int, limit: int) -> list[User]:
    """Search for users by email with optional pagination."""
    query = db.query(User)

    if search:
        query = query.filter(User.email.ilike(f"%{search}%"))

    return query.offset(offset).limit(limit).all()
