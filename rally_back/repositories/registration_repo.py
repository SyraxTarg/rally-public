"""This file contains the registration repository"""
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.registration_model import Registration
from models.event_model import Event

def get_number_registrations_for_event(db: Session, event_id: int)->int:
    """used to get the number of registrations from an event"""
    return db.query(Registration).filter(Registration.event_id == event_id).count()

def add_registration(db: Session, registration: Registration)->None:
    """used to add a registration in db"""
    db.add(registration)

def commit_registration(db: Session)->None:
    """used to commit changes"""
    db.commit()

def refresh_registration(db: Session, registration: Registration)->None:
    """used to refresh registration"""
    db.refresh(registration)

def get_registration_by_profile_and_event(db: Session, profile_id: int, event_id: int)->Optional[Registration]:
    """used to fetch a registration by its profile and event"""
    return db.query(Registration).filter(
        Registration.profile_id == profile_id,
        Registration.event_id == event_id
    ).first()
    
    
def get_all_registration_by_profile_and_event(db: Session, event_id: int)->list[Registration]:
    """used to fetch registrations by its event"""
    return db.query(Registration).filter(
        Registration.event_id == event_id
    ).all()

def get_registration_by_id(db: Session, registration_id: int)->Optional[Registration]:
    """used to fetch a registration by its id"""
    return db.query(Registration).filter(
        Registration.id == registration_id,
    ).first()

def delete_registration(db: Session, registration: Registration)->None:
    """used to delete a registration from db"""
    db.delete(registration)

def get_registrations_filters(
    db: Session,
    date: Optional[datetime],
    event_id: Optional[int],
    profile_id: Optional[int],
    offset: int,
    limit: int
)->list[Registration]:
    """used to fetch registrations from db according to given filters"""
    query = db.query(Registration)

    if date is not None:
        query = query.filter(func.date(Registration.registered_at) == date.date())

    if event_id is not None:
        query = query.filter(Registration.event_id == event_id)

    if profile_id is not None:
        query = query.filter(Registration.profile_id == profile_id)

    return query.order_by(Registration.registered_at.desc()).offset(offset).limit(limit).all()


def get_registrations_from_user(db: Session, profile_id: int, offset: int, limit: int)->list[Registration]:
    """used to fetch registrations according to their user"""
    return db.query(Registration).filter(Registration.profile_id == profile_id).offset(offset).limit(limit).all()

def get_count_registrations_from_user(db: Session, profile_id: int)->int:
    """used to fetch the total count of registrations for a user"""
    return db.query(Registration).filter(Registration.profile_id == profile_id).count()

def get_registrations_for_event_by_user(db: Session, profile_id: int, event_id: Optional[int], offset: int, limit: int)->list[Registration]:
    """used to fetch registrations from db according to their event and user"""
    query = db.query(Registration).join(Registration.event).filter(Event.profile_id == profile_id)

    if event_id:
        query = query.filter(Event.id == event_id)

    return query.offset(offset).limit(limit).all()
