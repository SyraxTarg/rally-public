from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status

from services import event_service, profile_service
from models.registration_model import Registration
from enums.payment_status import PaymentStatusEnum
from repositories import registration_repo
from errors import (
    RegistrationNotFound,
    EventNotFound,
    ProfileNotFound,
    RegistrationNotPossible
)



def get_number_registration_from_event(db: Session, event_id: int) -> int:
    """used to get the number of registration from an event"""
    event = event_service.get_event_by_id(db, event_id)

    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )

    return registration_repo.get_number_registrations_for_event(db, event_id)


def register_for_event(db: Session, profile_id: int, event_id: int) -> Registration:
    """used to create a registration for an event"""
    event = event_service.get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )
    profile = profile_service.get_profile(db, event.profile_id) if event else None

    if not profile:
        raise ProfileNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )

    registration = get_registration(db, profile_id, event_id)
    if not registration:
        registration = Registration(
            profile_id=profile_id,
            event_id=event_id,
            payment_status=PaymentStatusEnum.FREE
        )

        if ( event.date <= datetime.now()
            or event.cloture_billets < datetime.now()
        ):
            raise RegistrationNotPossible(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inscription impossible : date dépassée"
            )

        if get_number_registration_from_event(db, event.id) >= event.nb_places:
            raise RegistrationNotPossible(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inscription impossible : évènement complet"
            )

        registration_repo.add_registration(db, registration)
        registration_repo.commit_registration(db)
        registration_repo.refresh_registration(db, registration)

    return registration


def get_registration(db: Session, profile_id: int, event_id: int) -> Registration:
    """used to fetch a registration from event and profile"""
    return registration_repo.get_registration_by_profile_and_event(db, profile_id, event_id)


def get_all_registrations_from_event(db: Session, event_id: int) -> list[Registration]:
    """used to fetch a registration from event and profile"""
    return registration_repo.get_all_registration_by_profile_and_event(db, event_id)


def get_registration_by_id(db: Session, registration_id: int) -> Registration:
    """used to fetch registration by its id"""
    registration = registration_repo.get_registration_by_id(db, registration_id)
    if not registration:
        raise RegistrationNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )
    return registration


def delete_registration(db: Session, profile_id: int, event_id: int) -> bool:
    """used to delete a registration according to event and profile"""
    registration = get_registration(db, profile_id, event_id)

    if not registration:
        raise RegistrationNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )

    event = event_service.get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )
    profile = profile_service.get_profile(db, profile_id)
    if not profile:
        raise ProfileNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )

    registration_repo.delete_registration(db, registration)
    registration_repo.commit_registration(db)
    return True

def delete_registration_by_id(db: Session, registration_id: int) -> bool:
    """used to delete registration by its id"""
    registration = get_registration_by_id(db, registration_id)

    if not registration:
        raise RegistrationNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )

    event = event_service.get_event_by_id(db, registration.event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )
    profile = profile_service.get_profile(db, registration.profile_id)
    if not profile:
        raise ProfileNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )

    registration_repo.delete_registration(db, registration)
    registration_repo.commit_registration(db)
    return True

def get_registrations(
    db: Session,
    date: Optional[datetime],
    event_id: Optional[int],
    profile_id: Optional[int],
    offset: int,
    limit: int
)->list[Registration]:
    """used to fetch registrations according to given filters"""
    return registration_repo.get_registrations_filters(
        db,
        date,
        event_id,
        profile_id,
        offset,
        limit
    )

def get_registrations_for_user(
    db: Session,
    profile_id: int,
    offset: int,
    limit: int
) -> list[Registration]:
    """used to fetch registrations for a user"""
    registrations = registration_repo.get_registrations_from_user(db, profile_id, offset, limit)
    return registrations

def get_count_registrations_for_user(
    db: Session,
    profile_id: int,
) -> int:
    """used to fetch registrations for a user"""
    count = registration_repo.get_count_registrations_from_user(db, profile_id)
    return count

def update_registration_status(db: Session, status: PaymentStatusEnum, registration_id: int) -> Registration:
    """used to update the status of a registration"""
    registration = get_registration_by_id(db, registration_id)

    if not registration:
        raise RegistrationNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="la ressource n'existe pas"
        )

    registration.payment_status = status
    registration_repo.commit_registration(db)
    registration_repo.refresh_registration(db, registration)

    return registration

def get_registrations_for_events_by_user(
    db: Session,
    profile_id: int,
    event_id: Optional[int],
    offset: int,
    limit: int
)->list[Registration]:
    """used to fetch registrations for a event by a user"""
    return registration_repo.get_registrations_for_event_by_user(db, profile_id, event_id, offset, limit)
