"""This file contains the event picture repository"""
from sqlalchemy.orm import Session
from models.event_picture_model import EventPicture


def add_new_event_picture(db: Session, event_picture: EventPicture)->None:
    """
    This function adds a new event picture to the database.

    :param db: The database session used to interact with the database.
    :param event_picture: EventPicture object
    """
    db.add(event_picture)

def commit_event_picture(db: Session)->None:
    """
    This function commits an event picture to the database.

    :param db: The database session used to interact with the database.
    """
    db.commit()

def refresh_event_picture(db: Session, event_picture: EventPicture)->None:
    """
    This function updates the event picture in the database.

    :param db: Session object from SQLAlchemy for database operations
    :param event_picture: EventPicture object that represents an event picture in the database
    """
    db.refresh(event_picture)

def get_event_picture_by_id(db: Session, event_picture_id: int)->EventPicture:
    """
    This function retrieves an event picture by its ID from a database session.

    :param db: The database session used to interact with the database.
    :param id: This identifier is used to retrieve the specific event picture from the
    database
    """
    return db.query(EventPicture).filter(EventPicture.id == event_picture_id).first()

def get_all_event_pictures(db: Session)->list[EventPicture]:
    """
    This function retrieves all event pictures from the database.

    :param db: The database session used to interact with the database.
    """
    return db.query(EventPicture).all()

def get_event_pictures_from_event_id(db: Session, event_id: int)->list[EventPicture]:
    """
    This function retrieves a list of event pictures associated with a specific event ID from a database
    session.

    :param db: The database session used to interact with the database.
    :param event_id: It is used to retrieve event pictures associated with a specific event from the database
    """
    return db.query(EventPicture).filter(EventPicture.event_id == event_id).all()

def get_first_picture_of_event(db: Session, event_id: int)->EventPicture:
    """
    This function retrieves the first picture associated with a specific event from the database.

    :param db: The database session used to interact with the database.
    :param event_id: This identifier is used to retrieve the first picture associated with that
    event
    """
    return db.query(EventPicture).filter(EventPicture.event_id == event_id).first()

def delete_event_picture(db: Session, event_picture: EventPicture)->None:
    """
    This function deletes an event picture from the database.

    :param db: The database session used to interact with the database.
    :param event_picture: EventPicture object
    """
    db.delete(event_picture)

def get_picture_by_name(db: Session, name: str)->EventPicture:
    """
    This function retrieves an EventPicture from the database based on the provided name.

    :param db: The database session used to interact with the database.
    :param name: The `name` parameter is a string that represents the name of the picture you want to
    retrieve from the database
    """
    return db.query(EventPicture).filter(EventPicture.photo == name).first()
