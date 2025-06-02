import os
from sqlalchemy.orm import Session
from fastapi import status
from models.event_picture_model import EventPicture
from repositories import event_picture_repo
from errors import PictureNotFoundError


def create_event_picture(db: Session, event_id: int, photo: str)->EventPicture:
    """used to add an event picture"""
    new_picture = EventPicture(
        event_id=event_id,
        photo=photo
    )
    event_picture_repo.add_new_event_picture(db, new_picture)
    event_picture_repo.commit_event_picture(db)
    event_picture_repo.refresh_event_picture(db, new_picture)
    return new_picture

def get_picture_by_id(db: Session, picture_id: int)->EventPicture:
    """used to get a picture by its id"""
    picture = event_picture_repo.get_event_picture_by_id(db, picture_id)
    if not picture:
        raise PictureNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Picture not found"
        )
    return picture

def get_pictures(db: Session)->list[EventPicture]:
    """used to fetch all pictures"""
    return event_picture_repo.get_all_event_pictures(db)

def get_pictures_from_event(db: Session, event_id)->list[EventPicture]:
    """used to fetch pictures from an event"""
    return event_picture_repo.get_event_pictures_from_event_id(db, event_id)

def get_first_picture_of_event(db: Session, event_id: int)->EventPicture:
    """used to fetch the first picture for an event"""
    return event_picture_repo.get_first_picture_of_event(db, event_id)

def delete_picture(db: Session, picture_id: int)->None:
    """used to delete a picture"""
    picture = get_picture_by_id(db, picture_id)
    if not picture:
        raise PictureNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Picture not found"
        )
    event_picture_repo.delete_event_picture(db, picture)
    event_picture_repo.commit_event_picture(db)

def get_picture_by_name(db: Session, name: str)->EventPicture:
    """used to fetch a picture by its name"""
    return event_picture_repo.get_picture_by_name(db, name)

def add_picture_to_event(db: Session, names: list[str], event_id: int):
    """used to link a picture to an event"""
    for name in names:
        picture = get_picture_by_name(db, name)
        if not picture:
            picture = create_event_picture(db, event_id, name)
        picture.event_id = event_id
        event_picture_repo.commit_event_picture(db)
        event_picture_repo.refresh_event_picture(db, picture)

def delete_pictures(db: Session, names: list[str]) -> None:
    """used to delete pictures"""
    for name in names:
        picture = get_picture_by_name(db, name)
        event_picture_repo.delete_event_picture(db, picture)
    event_picture_repo.commit_event_picture(db)
