"""This file contains the like repository"""
from sqlalchemy.orm import Session
from models.like_model import Like

def add_like(db: Session, like: Like)->None:
    """
    This function is used to add a like in db.
    """
    db.add(like)

def commit_like(db: Session)->None:
    """
    This function is used to commit the changes in db.
    """
    db.commit()

def refresh_like(db: Session, like: Like)->None:
    """
    This function is used to refresh a like object in the db.
    """
    db.refresh(like)

def get_like_by_profile_and_event(db: Session, profile_id: int, event_id: int)->Like:
    """
    This function is used to fetch a like according to its profile and event.
    """
    return db.query(Like).filter(
        Like.profile_id == profile_id,
        Like.event_id == event_id
    ).first()

def delete_like(db: Session, like: Like)->None:
    """
    This function is used to delete a like in db.
    """
    db.delete(like)

def get_likes(db: Session, offset: int, limit: int)->list[Like]:
    """
    This function is used de fetch all the likes from db.
    """
    return db.query(Like).offset(offset).limit(limit).all()

def get_likes_from_event(db: Session, event_id: int)->list[Like]:
    """
    This function is used to fetch likes from db according to their events.
    """
    return db.query(Like).filter(Like.event_id == event_id).all()

def get_likes_from_profile(db: Session, profile_id: int)->list[Like]:
    """
    This function is used to fetch likes from db according to their profiles.
    """
    return db.query(Like).filter(Like.profile_id == profile_id).all()
