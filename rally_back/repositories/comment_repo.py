"""This file contains the comment repository"""
from sqlalchemy.orm import Session
from models.comment_model import Comment


def add_new_comment(db: Session, comment: Comment)->None:
    """
    Adding a new comment in database.

    Args:
        db (Session): The database session used to interact with the database.
        comment (Comment): The comment we want to add.
    """
    db.add(comment)

def commit_comment(db: Session)->None:
    """
    Commiting changes in the database

    Args:
        db (Session): The database session used to interact with the database.
    """
    db.commit()

def delete_comment(db: Session, comment: Comment)->None:
    """
    Deleting a comment from the database.

    Args:
        db (Session): The database session used to interact with the database.
        comment (Comment): The comment we want to delete.
    """
    db.delete(comment)

def refresh_comment(db: Session, comment: Comment)->None:
    """
    Refreshing an object

    Args:
        db (Session): The database session used to interact with the database.
        comment (Comment): The comment to refresh
    """
    db.refresh(comment)

def get_comment_by_event_id(db: Session, event_id: int, offset: int, limit: int)->list[Comment]:
    """
    Fetching comments by their event.

    Args:
        db (Session): The database session used to interact with the database.
        event_id (int): The id of the event
        offset (int): offset for pagination
        limit (int): limit for pagination

    Returns:
        list[Comment]
    """
    return db.query(Comment).filter(Comment.event_id == event_id).offset(offset).limit(limit).all()


def get_all_comments_by_event_id(db: Session, event_id: int)->list[Comment]:
    """
    Fetching comments by their event.

    Args:
        db (Session): The database session used to interact with the database.
        event_id (int): The id of the event
        offset (int): offset for pagination
        limit (int): limit for pagination

    Returns:
        list[Comment]
    """
    return db.query(Comment).filter(Comment.event_id == event_id).all()

def get_all_comments(db: Session, offset: int, limit: int)->list[Comment]:
    """
    Fetching all the comments.

    Args:
        db (Session): The database session used to interact with the database.
        offset (int): offset for pagination
        limit (int): limit for pagination

    Returns:
        list[Comment]
    """
    return db.query(Comment).offset(offset).limit(limit).all()

def get_comment_by_id(db: Session, comment_id: int)->Comment:
    """
    Fetching comment by its id.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): comment id

    Returns:
        Comment
    """
    return db.query(Comment).filter(Comment.id == comment_id).first()

def get_comments_by_profile_id(db: Session, profile_id: int, offset: int, limit: int)->list[Comment]:
    """
    Fetching comments by their profile.

    Args:
        db (Session): The database session used to interact with the database.
        profile_id (int): profile id
        offset (int): offset for pagination
        limit (int): limit for pagination

    Returns:
        list[Comment]
    """
    return db.query(Comment).filter(Comment.profile_id == profile_id).offset(offset).limit(limit).all()
