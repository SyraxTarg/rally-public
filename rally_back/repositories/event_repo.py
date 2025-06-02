"""This file contains the event repository"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import or_, case, func
from models.event_model import Event
from models.address_model import Address
from models.type_model import Type
from models.profile_model import Profile


def add_new_event(db: Session, event: Event)->None:
    """
    This function adds a new event to the database.

    :param db: The database session used to interact with the database.
    :param event: Event object to add
    """
    db.add(event)

def commit_event(db: Session)->None:
    """
    This function commits an event to the database using the provided session.

    :param db: The database session used to interact with the database.
    """
    db.commit()

def refresh_event(db: Session, event: Event)->None:
    """
    This function refreshes the data of a specific event in the database.

    :param db:The database session used to interact with the database.
    :param event: Event object
    """
    db.refresh(event)

def delete_event(db: Session, event: Event)->None:
    """
    This function deletes a specific event from the database.

    :param db: The database session used to interact with the database.
    :param event: Event object to delete.
    """
    db.delete(event)

def get_event_by_id(db: Session, event_id: int)->Event:
    """
    This function retrieves an event from a database by its ID.

    :param db: The database session used to interact with the database.
    :param id: The `id` parameter is an integer that represents the unique identifier of the event you
    want to retrieve from the database
    """
    return db.query(Event).filter(Event.id == event_id).first()

def get_events_by_profile(db: Session, profile_id: int, offset: int, limit: int)->list[Event]:
    """
    This function retrieves a list of events associated with a specific profile, with optional offset
    and limit parameters.

    :param db: The database session used to interact with the database.
    :param profile_id: This identifier is used to retrieve events associated with a
    specific user profile
    :param offset: offset for pagination
    :param limit: limit for pagination
    """
    return db.query(Event).filter(Event.profile_id == profile_id).offset(offset).limit(limit).all()


def get_all_events_by_profile(db: Session, profile_id: int)->list[Event]:
    """
    This function retrieves a list of events associated with a specific profile, with optional offset
    and limit parameters.

    :param db: The database session used to interact with the database.
    :param profile_id: This identifier is used to retrieve events associated with a
    specific user profile
    :param offset: offset for pagination
    :param limit: limit for pagination
    """
    return db.query(Event).filter(Event.profile_id == profile_id).all()


def get_events_filters(
    db: Session,
    date_avant: Optional[datetime],
    date_apres: Optional[datetime],
    type_ids: Optional[list[int]],
    profile_id: Optional[int],
    country: Optional[str],
    city: Optional[str],
    popularity: Optional[bool],
    recent: Optional[bool],
    nb_places: Optional[int],
    search: Optional[str],
    offset: int,
    limit: int
)->list[Event]:
    """
    This function takes various filters as input parameters and returns a list of events based on those
    filters.
    """
    query = db.query(Event)

    if date_avant is not None:
        query = query.filter(func.date(Event.date) <= date_avant.date())

    if date_apres is not None:
        query = query.filter(func.date(Event.date) >= date_apres.date())

    if type_ids:
        query = query.join(Event.types).filter(Type.id.in_(type_ids)).group_by(Event.id)

        query = query.order_by(
            case(
                (
                    func.count(func.distinct(Type.id)) == len(type_ids), 0
                ),
                else_=1
            )
        )

    if profile_id is not None:
        query = query.filter(Event.profile_id == profile_id)

    if country is not None:
        query = query.join(Event.address).filter(Address.country == country)

    if city is not None:
        query = query.join(Event.address).filter(Address.city == city)

    if search is not None:
        query = query.join(Event.address)
        query = query.join(Event.profile)
        query = query.filter(
            or_(
                Event.title.ilike(f"%{search}%"),
                Event.description.ilike(f"%{search}%"),
                Address.city.ilike(f"%{search}%"),
                Address.country.ilike(f"%{search}%"),
                Address.zipcode.ilike(f"%{search}%"),
                Profile.first_name.ilike(f"%{search}%"),
                Profile.last_name.ilike(f"%{search}%"),
                # Type.type.ilike(f"%{search}%")
            )
        )

    if popularity:
        query = query.order_by(Event.nb_likes.desc())

    if recent:
        query = query.order_by(Event.created_at.desc())

    if nb_places:
        query = query.order_by(
            case(
                (Event.nb_places == nb_places, 0),
                else_=1
            )
        )

    return query.offset(offset=offset).limit(limit=limit)

def get_events_filters_total_count(
    db: Session,
    date_avant: Optional[datetime],
    date_apres: Optional[datetime],
    type_ids: Optional[list[int]],
    profile_id: Optional[int],
    country: Optional[str],
    city: Optional[str],
    search: Optional[str]
)->int:
    """
    This function takes various filters as input parameters and returns a list of events based on those
    filters.
    """
    query = db.query(Event)

    if date_avant is not None:
        query = query.filter(func.date(Event.date) <= date_avant.date())

    if date_apres is not None:
        query = query.filter(func.date(Event.date) >= date_apres.date())

    if type_ids:
        query = query.join(Event.types).filter(Type.id.in_(type_ids)).group_by(Event.id)

    if profile_id is not None:
        query = query.filter(Event.profile_id == profile_id)

    if country is not None:
        query = query.join(Event.address).filter(Address.country == country)

    if city is not None:
        query = query.join(Event.address).filter(Address.city == city)

    if search is not None:
        query = query.join(Event.address)
        query = query.join(Event.profile)
        query = query.join(Event.types)
        query = query.filter(
            or_(
                Event.title.ilike(f"%{search}%"),
                Event.description.ilike(f"%{search}%"),
                Address.city.ilike(f"%{search}%"),
                Address.country.ilike(f"%{search}%"),
                Address.zipcode.ilike(f"%{search}%"),
                Profile.first_name.ilike(f"%{search}%"),
                Profile.last_name.ilike(f"%{search}%"),
                Type.type.ilike(f"%{search}%")
            )
        )

    return query.distinct(Event.id).count()
