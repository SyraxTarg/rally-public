"""This file contains the banned user repository"""
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from models.banned_user_model import BannedUser


def add_new_banned_user(db: Session, banned_user: BannedUser)->None:
    """
    Adding a new banned user in the database

    Args:
        db (Session): The database session used to interact with the database.
        banned_user (BannedUser): The banned user object to add.
    """
    db.add(banned_user)

def commit_banned_user(db: Session)->None:
    """
    Commiting the changes from the database

    Args:
        db (Session): The database session used to interact with the database.
    """
    db.commit()

def refresh_banned_user(db: Session, banned_user: BannedUser)->None:
    """
    Refreshing an object from the database.

    Args:
        db (Session): The database session used to interact with the database.
        banned_user (BannedUser): The banned user to refresh.
    """
    db.refresh(banned_user)

def get_banned_user_by_email(db: Session, email: str)->Optional[BannedUser]:
    """
    Fetching a banned user from the database according to a given email.

    Args:
        db (Session): The database session used to interact with the database.
        email (str): The banned user email.

    Returns:
        Optional[BannedUser]
    """
    return db.query(BannedUser).filter(func.lower(BannedUser.banned_email) == email.lower()).first()

def delete_banned_user(db: Session, banned_user: BannedUser)->None:
    """
    Deleting a banned user from the database.

    Args:
        db (Session): The database session used to interact with the database.
        banned_user (BannedUser): The banned user we want to delete.
    """
    db.delete(banned_user)

def get_all_banned_emails(db: Session, offset: int, limit: int)-> list[BannedUser]:
    """
    Fetching all the banned users from the database.

    Args:
        db (Session): The database session used to interact with the database.
        offset (int): offset for pagination
        limit (int): limit for pagination

    Returns:
        list[BannedUser]
    """
    return db.query(BannedUser).offset(offset).limit(limit).all()
