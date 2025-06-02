"""
This file contains the controller related to registrations
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from schemas.response_schemas.profile_schema_response import ProfileRestrictedSchemaResponse
from services import (
    action_log_service,
    event_service,
    profile_service,
    registration_service,
    user_service
)
from schemas.request_schemas.registration_schema import RegistrationSchema
from schemas.response_schemas.registration_schema_response import (
    RegistrationSchemaResponseSchemas,
    RegistrationNumberSchemaResponseSchemas,
    RegistrationListSchemaResponseSchemas,
    IsUserRegistered
)
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum
from models.user_model import User


def register_event_current_user(db: Session, current_user: User, registration: RegistrationSchema) -> RegistrationSchemaResponseSchemas:
    """
    Registers the current user for an event.

    Args:
        db (Session): The database session used to interact with the database.
        current_user (User): The user performing the registration.
        registration (RegistrationSchema): The registration data for the event, including the event ID.

    Returns:
        RegistrationSchemaResponseSchemas: A schema response containing the registration details including the user profile, event ID, registration time, and payment status.

    This function registers the user for the specified event, logs the action, and returns the registration details.
    """
    new_registration = registration_service.register_for_event(db, current_user.id, registration.event_id)

    profile = profile_service.get_profile(db, current_user.id)

    user = user_service.get_user(db, profile.user_id)

    profile_schema = ProfileRestrictedSchemaResponse(
        id=profile.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        photo=profile.photo,
        nb_like=profile.nb_like,
        email=user.email,
        created_at=profile.created_at,
    )

    event = event_service.get_event_by_id(db, registration.event_id)

    action_log_service.create_action_log(
        db,
        current_user.id,
        LogLevelEnum.INFO,
        ActionEnum.EVENT_REGISTERED,
        f"Profile {profile.id} registered to event {event.id} at {new_registration.registered_at} by {current_user.email}"
    )

    return RegistrationSchemaResponseSchemas(
        id=new_registration.id,
        profile=profile_schema,
        event_id=event.id,
        event_title=event.title,
        registered_at=new_registration.registered_at,
        payment_status=new_registration.payment_status
    )


def get_registrations(
    db: Session,
    event_id: Optional[int],
    profile_id: Optional[int],
    date: Optional[datetime],
    offset: int,
    limit: int
)  -> RegistrationListSchemaResponseSchemas:
    """
    Retrieves a list of registrations based on provided filters.

    Args:
        db (Session): The database session used to interact with the database.
        event_id (Optional[int]): The ID of the event to filter registrations by.
        profile_id (Optional[int]): The ID of the profile to filter registrations by.
        date (Optional[datetime]): The date filter for registrations.
        offset (int): The number of items to skip for pagination.
        limit (int): The number of items to retrieve for pagination.

    Returns:
        RegistrationListSchemaResponseSchemas: A schema response containing a list of registrations with the profile and event details.

    This function fetches all registrations matching the given filters, including related profile and event information.
    """
    registrations = registration_service.get_registrations(
        db,
        date,
        event_id,
        profile_id,
        offset,
        limit
    )

    all_registrations = []

    for registration in registrations:
        profile = profile_service.get_profile(db, registration.profile_id)

        user = user_service.get_user(db, profile.user_id)

        profile_schema = ProfileRestrictedSchemaResponse(
            id=profile.id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            photo=profile.photo,
            nb_like=profile.nb_like,
            email=user.email,
            created_at=profile.created_at,
        )

        event = event_service.get_event_by_id(db, registration.event_id)

        all_registrations.append(RegistrationSchemaResponseSchemas(
            id=registration.id,
            profile=profile_schema,
            event_id=event.id,
            registered_at=registration.registered_at,
            payment_status=registration.payment_status
        ))

    return RegistrationListSchemaResponseSchemas(
        count=len(all_registrations),
        data=all_registrations
    )


def get_number_places_from_event(db: Session, event_id: int) -> RegistrationNumberSchemaResponseSchemas:
    """
    Retrieves the number of registrations for a specific event.

    Args:
        db (Session): The database session used to interact with the database.
        event_id (int): The ID of the event for which the number of registrations is requested.

    Returns:
        RegistrationNumberSchemaResponseSchemas: A schema response containing the event ID and the number of registrations.

    This function fetches the total number of registrations associated with the given event ID.
    """
    number = registration_service.get_number_registration_from_event(db, event_id)

    return RegistrationNumberSchemaResponseSchemas(
        id= event_id,
        number=number
    )


def get_registration(db: Session, event_id: int, profile_id: int) -> RegistrationSchemaResponseSchemas:
    """
    Retrieves a specific registration for a profile on a particular event.

    Args:
        db (Session): The database session used to interact with the database.
        event_id (int): The ID of the event for which the registration is being queried.
        profile_id (int): The ID of the profile for which the registration is being queried.

    Returns:
        RegistrationSchemaResponseSchemas: A schema response containing the registration details,
        including profile information, event ID, registration date, and payment status.

    This function retrieves the registration details for a given profile and event, including the associated profile and event data.
    """
    registration = registration_service.get_registration(db, profile_id, event_id)

    profile = profile_service.get_profile(db, profile_id)

    user = user_service.get_user(db, profile.user_id)

    profile_schema = ProfileRestrictedSchemaResponse(
        id=profile.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        photo=profile.photo,
        nb_like=profile.nb_like,
        email=user.email,
        created_at=profile.created_at,
    )

    event = event_service.get_event_by_id(db, registration.event_id)

    return RegistrationSchemaResponseSchemas(
        id=registration.id,
        profile=profile_schema,
        event=event.id,
        registered_at=registration.registered_at,
        payment_status=registration.payment_status
    )


def get_registration_by_id(db: Session, registration_id: int) -> RegistrationSchemaResponseSchemas:
    """
    Retrieves a registration by its unique ID and includes the associated profile and event details.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): The ID of the registration to retrieve.

    Returns:
        RegistrationSchemaResponseSchemas: A schema response containing the registration details,
        including profile information, event ID, registration date, and payment status.

    This function retrieves the registration details for a given registration ID, including the associated profile and event data.
    """
    registration = registration_service.get_registration_by_id(db, registration_id)

    profile = profile_service.get_profile(db, registration.profile_id)
    user = user_service.get_user(db, profile.user_id)

    profile_schema = ProfileRestrictedSchemaResponse(
        id=profile.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        photo=profile.photo,
        nb_like=profile.nb_like,
        email=user.email,
        created_at=profile.created_at,
    )

    event = event_service.get_event_by_id(db, registration.event_id)

    return RegistrationSchemaResponseSchemas(
        id=registration.id,
        profile=profile_schema,
        event_id=event.id,
        registered_at=registration.registered_at,
        payment_status=registration.payment_status
    )


def delete_registration(db: Session, profile_id: int, event_id: int, current_user: User) -> dict[str, str]:
    """
    Deletes a registration of a user for a specific event and logs the action.

    Args:
        db (Session): The database session used to interact with the database.
        profile_id (int): The ID of the profile to unregister from the event.
        event_id (int): The ID of the event to unregister from.
        current_user (User): The current user performing the action (for logging purposes).

    Returns:
        dict: A dictionary with a message indicating the registration was deleted.

    This function removes a user's registration for an event and logs the action with the current user's details.
    """
    registration_service.delete_registration(db, profile_id, event_id)
    action_log_service.create_action_log(
        db,
        current_user.id,
        LogLevelEnum.INFO,
        ActionEnum.EVENT_UNREGISTERED,
        f"Profile {profile_id} unregistered for event {event_id} by {current_user.email}"
    )
    return {"msg": "deleted"}


def get_registrations_for_current_user(db: Session, current_user: User, offset: int, limit: int) -> RegistrationListSchemaResponseSchemas:
    """
    Retrieves the list of event registrations for the current user, including related profile and event details.

    Args:
        db (Session): The database session used to interact with the database.
        current_user (User): The current user for whom the registrations are being retrieved.
        offset (int): The number of registrations to skip (for pagination).
        limit (int): The maximum number of registrations to return (for pagination).

    Returns:
        RegistrationListSchemaResponseSchemas: A response containing the count and list of registrations with related details.
    """
    registrations = registration_service.get_registrations_for_user(
        db,
        current_user.id,
        offset,
        limit
    )

    all_registrations = []

    for registration in registrations:
        profile = profile_service.get_profile(db, registration.profile_id)
        user = user_service.get_user(db, profile.user_id)

        profile_schema = ProfileRestrictedSchemaResponse(
            id=profile.id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            photo=profile.photo,
            nb_like=profile.nb_like,
            email=user.email,
            created_at=profile.created_at,
        )

        event = event_service.get_event_by_id(db, registration.event_id)


        all_registrations.append(RegistrationSchemaResponseSchemas(
            id=registration.id,
            profile=profile_schema,
            event_id=event.id,
            event_title=event.title,
            registered_at=registration.registered_at,
            payment_status=registration.payment_status
        ))

    return RegistrationListSchemaResponseSchemas(
        count=len(all_registrations),
        total=registration_service.get_count_registrations_for_user(db, current_user.id),
        data=all_registrations
    )


def get_registrations_for_event_by_user(
    db: Session,
    current_user: User,
    event_id: Optional[int],
    offset: int,
    limit: int
) -> RegistrationListSchemaResponseSchemas:
    """
    Retrieves the list of event registrations for a specific user, filtered by event, including related profile and event details.

    Args:
        db (Session): The database session used to interact with the database.
        current_user (User): The current user for whom the registrations are being retrieved.
        event_id (Optional[int]): The event ID to filter the registrations (can be None for all events).
        offset (int): The number of registrations to skip (for pagination).
        limit (int): The maximum number of registrations to return (for pagination).

    Returns:
        RegistrationListSchemaResponseSchemas: A response containing the count and list of registrations with related details.
    """
    registrations = registration_service.get_registrations_for_events_by_user(
        db,
        current_user.id,
        event_id,
        offset,
        limit
    )

    all_registrations = []

    for registration in registrations:
        profile = profile_service.get_profile(db, registration.profile_id)
        user = user_service.get_user(db, profile.user_id)

        profile_schema = ProfileRestrictedSchemaResponse(
            id=profile.id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            photo=profile.photo,
            nb_like=profile.nb_like,
            email=user.email,
            created_at=profile.created_at,
        )

        event = event_service.get_event_by_id(db, registration.event_id)

        all_registrations.append(RegistrationSchemaResponseSchemas(
            id=registration.id,
            profile=profile_schema,
            event_id=event.id,
            event_title=event.title,
            registered_at=registration.registered_at,
            payment_status=registration.payment_status
        ))

    return RegistrationListSchemaResponseSchemas(
        count=len(all_registrations),
        total=registration_service.get_count_registrations_for_user(db, current_user.id),
        data=all_registrations
    )

def is_user_registered(db: Session, event_id: int, user_id: int)->IsUserRegistered:
    """function to know if user is registered to event"""
    if registration_service.get_registration(db, user_id, event_id):
        return IsUserRegistered(
            registered=True
        )
    else:
        return IsUserRegistered(
            registered=False
        )
