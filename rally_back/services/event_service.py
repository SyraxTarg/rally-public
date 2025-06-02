from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status

from models.event_model import Event
from services import bad_words_service
from repositories import event_repo, type_repo
from errors import EventNotFound, InvalidContent




def create_event(
    db: Session,
    title: str,
    description: str,
    nb_places: int,
    price: float,
    profile_id: int,
    date: datetime,
    cloture_billets: datetime,
    types: list[int],
    address_id: int
)->Event:
    """used to create an event"""
    if not bad_words_service.is_content_clean(title) or not bad_words_service.is_content_clean(description):
        raise InvalidContent(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Event contains invalid terms"
        )

    new_event = Event(
        title=title,
        description=description,
        nb_places=nb_places,
        price=price,
        profile_id=profile_id,
        nb_likes=0,
        nb_comments=0,
        date=date,
        cloture_billets=cloture_billets,
        address_id=address_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    event_repo.add_new_event(db, new_event)
    event_repo.commit_event(db)
    add_types_to_event(db, new_event.id, types)
    event_repo.refresh_event(db, new_event)
    return new_event

def get_event_by_id(db: Session, event_id: int)->Event:
    """used to fetch an event by its id"""
    event = event_repo.get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="event does not exist"
        )
    return event

def update_event(
    db: Session,
    event_id: int,
    title: str,
    description: str,
    nb_places: int,
    price: float,
    date: datetime,
    cloture_billets: datetime,
    types: list[int]
)->Event:
    """used to update an event"""
    event = get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="event does not exist"
        )
    event.title = title
    event.description = description
    event.nb_places = nb_places
    event.price = price
    event.date = date
    event.cloture_billets = cloture_billets
    event.updated_at = datetime.now()
    event_types_ids = {t.id for t in event.types}

    types_to_remove = event_types_ids - set(types)
    types_to_add = set(types) - event_types_ids
    add_types_to_event(db, event_id, types_to_add)
    remove_types_to_event(db, event_id, types_to_remove)

    event_repo.commit_event(db)
    event_repo.refresh_event(db, event)
    return event

def add_types_to_event(db: Session, event_id: int, types: list[int])->Event:
    """used to add types to an event"""
    event = get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="event does not exist"
        )

    for t in types:
        type_ = type_repo.get_type_by_id(db, t)
        if type_  in event.types:
            continue
        event.types.append(type_)

    event_repo.commit_event(db)
    return event

def remove_types_to_event(db: Session, event_id: int, types: list[int])->Event:
    """used to remove types from event"""
    event = get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="event does not exist"
        )

    for t in types:
        type_ = type_repo.get_type_by_id(db, t)
        if not type_:
            continue

        if type_  in event.types:
            event.types.remove(type_)

    event_repo.commit_event(db)
    return event

def get_events_by_profile(db: Session, profile_id: int, offset: int, limit: int) -> list[Event]:
    """used to fetch event by their profile"""
    return event_repo.get_events_by_profile(db, profile_id, offset, limit)


def get_all_events_by_profile(db: Session, profile_id: int) -> list[Event]:
    """used to fetch all events by their profile"""
    return event_repo.get_all_events_by_profile(db, profile_id)


def get_events_filters(
    db: Session,
    date_avant: Optional[datetime] = None,
    date_apres: Optional[datetime] = None,
    type_ids: Optional[list[int]] = None,
    profile_id: Optional[int] = None,
    country: Optional[str] = None,
    city: Optional[str] = None,
    popularity: Optional[bool] = None,
    recent: Optional[bool] = None,
    nb_places: Optional[int] = None,
    search: Optional[str] = None,
    offset: int = 0,
    limit: int = 5
) -> list[Event]:
    """used to fetch events according to given filters"""
    return event_repo.get_events_filters(
        db,
        date_avant,
        date_apres,
        type_ids,
        profile_id,
        country,
        city,
        popularity,
        recent,
        nb_places,
        search,
        offset,
        limit
    )

def get_count_total_events(
    db: Session,
    date_avant: Optional[datetime] = None,
    date_apres: Optional[datetime] = None,
    type_ids: Optional[list[int]] = None,
    profile_id: Optional[int] = None,
    country: Optional[str] = None,
    city: Optional[str] = None,
    search: Optional[str] = None
)->int:
    """used to fetch count of events according to given filters"""
    return event_repo.get_events_filters_total_count(
        db,
        date_avant,
        date_apres,
        type_ids,
        profile_id,
        country,
        city,
        search
    )