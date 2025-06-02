from typing import Optional
from datetime import datetime
from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from controllers import authent_controller
from database.db import get_db
from models.user_model import User
from controllers import registration_controller
from schemas.request_schemas.registration_schema import RegistrationSchema
from schemas.response_schemas.registration_schema_response import (
    RegistrationNumberSchemaResponseSchemas,
    RegistrationSchemaResponseSchemas,
    RegistrationListSchemaResponseSchemas,
    IsUserRegistered
)

router = APIRouter(
    prefix="/api/v1/registrations",
    tags=["registration"],
)

@router.post("/", response_model=RegistrationSchemaResponseSchemas, status_code=201)
def register_to_event(
    registration: RegistrationSchema,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> RegistrationSchemaResponseSchemas:
    """Register the current user to an event."""
    return registration_controller.register_event_current_user(db, current_user, registration)


@router.get("/", response_model=RegistrationListSchemaResponseSchemas, status_code=201)
def get_registrations(
    event_id: Optional[int] = Query(None),
    profile_id: Optional[int] = Query(None),
    date: Optional[datetime] = Query(None),
    offset: int = Query(0),
    limit: int = Query(5),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> RegistrationListSchemaResponseSchemas:
    """Get a list of registrations, optionally filtered by event, profile, or date. Accessible to admin or super-admin."""
    return registration_controller.get_registrations(db, event_id, profile_id, date, offset, limit)


@router.get("/places/{event_id}", response_model=RegistrationNumberSchemaResponseSchemas, status_code=201)
def get_count_registrations_for_event(
    event_id: int,
    db: Session = Depends(get_db)
) -> RegistrationNumberSchemaResponseSchemas:
    """Get the count of registrations for a specific event."""
    return registration_controller.get_number_places_from_event(db, event_id)


@router.get("/fetch", response_model=RegistrationSchemaResponseSchemas, status_code=201)
def get_registration(
    event_id: Optional[int] = Query(None),
    profile_id: Optional[int] = Query(None),
    _: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> RegistrationSchemaResponseSchemas:
    """Fetch a specific registration by event and profile ID."""
    return registration_controller.get_registration(db, event_id, profile_id)


@router.get("/self", response_model=RegistrationListSchemaResponseSchemas, status_code=200)
def get_registrations_current_user(
    offset: int = Query(0),
    limit: int = Query(5),
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> RegistrationSchemaResponseSchemas:
    """Get a list of registrations for the current user."""
    return registration_controller.get_registrations_for_current_user(db, current_user, offset, limit)


@router.get("/self/events", response_model=RegistrationListSchemaResponseSchemas, status_code=200)
def get_registrations_event_by_current_user(
    offset: int = Query(0),
    limit: int = Query(5),
    event_id: Optional[int] = Query(None),
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> RegistrationSchemaResponseSchemas:
    """Get a list of registrations for events by the current user, optionally filtered by event ID."""
    return registration_controller.get_registrations_for_event_by_user(db, current_user, event_id, offset, limit)


@router.get("/is-registered", response_model=IsUserRegistered, status_code=200)
def is_user_registered(
    event_id: int = Query,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> IsUserRegistered:
    """Know if the curret user is registered for an event"""
    return registration_controller.is_user_registered(db, event_id, current_user.id)


@router.get("/{registration_id}", response_model=RegistrationSchemaResponseSchemas, status_code=201)
def get_registration_by_id(
    registration_id: int,
    _: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> RegistrationSchemaResponseSchemas:
    """Get a specific registration by its ID."""
    return registration_controller.get_registration_by_id(db, registration_id)


@router.delete("/", response_model=dict[str, str], status_code=200)
def delete_registration(
    profile_id: int = Query,
    event_id: int = Query,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> RegistrationSchemaResponseSchemas:
    """Delete a registration by profile ID and event ID."""
    return registration_controller.delete_registration(db, profile_id, event_id, current_user)


@router.delete("/self", response_model=dict[str, str], status_code=200)
def delete_registration_current_user(
    event_id: int = Query,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> RegistrationSchemaResponseSchemas:
    """Delete the current user's registration from a specific event."""
    return registration_controller.delete_registration(db, current_user.id, event_id)
