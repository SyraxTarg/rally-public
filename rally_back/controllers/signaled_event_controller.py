"""
This file contains the controller related to signaled signaled events
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from schemas.request_schemas.signaled_event_schema import SignaledEventByCurrentUserSchema
from schemas.response_schemas.reason_schema_response import ReasonSchemaResponse
from schemas.response_schemas.signaled_event_schema_response import SignaledEventSchemaResponse, SignaledEventListSchemaResponse
from schemas.response_schemas.user_schema_response import UserResponse
from schemas.response_schemas.role_schema_response import RoleSchemaResponse
from schemas.response_schemas.profile_schema_response import  ProfileRestrictedSchemaResponse
from schemas.response_schemas.type_schema_response import TypeSchemaResponse
from schemas.response_schemas.event_picture_schema_response import EventPictureSchemaResponse
from schemas.response_schemas.address_schema_response import AddressSchemaResponse
from schemas.response_schemas.event_schema_response import EventSchemaResponse
from services import (
    action_log_service,
    event_picture_service,
    event_service,
    moderation_service,
    profile_service,
    reason_service,
    role_service,
    signaled_event_service,
    type_service,
    user_service
)
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum
from models.user_model import User


def create_signaled_event_by_current_user(
    db: Session,
    signaled_event: SignaledEventByCurrentUserSchema,
    current_user: User
) -> bool:
    """
    Creates a signaled event by the current user. This function allows a user to signal an event as inappropriate
    by specifying the event, reason for signaling, and the user who is reporting it.

    Args:
        db (Session): The database session used to perform the database operations.
        signaled_event (SignaledEventByCurrentUserSchema): The data representing the event being signaled and the reason for signaling.
        current_user (User): The current logged-in user who is signaling the event.

    Returns:
        bool: Returns True if the signaled event is successfully created, otherwise returns False.
    """
    return  signaled_event_service.create_signaled_event(
        db=db,
        event_id=signaled_event.event_id,
        user_id=current_user.id,
        reason_id=signaled_event.reason_id
    )

def get_signaled_events(db: Session) -> SignaledEventListSchemaResponse:
    """
    Retrieves a list of signaled events from the database. Each event contains detailed information
    about the event itself, the user who signaled it, and the reason for signaling.

    Args:
        db (Session): The database session used for querying data.

    Returns:
        SignaledEventListSchemaResponse: A response schema containing the list of signaled events,
        including detailed event information, the user who signaled the event, and the reason.
    """
    signaled_events = signaled_event_service.get_signaled_events(db)

    all_signaled_events = []

    for signaled_comment in signaled_events:
        signaled_by = user_service.get_user(db, signaled_comment.user_id)

        reason = reason_service.get_reason_by_id(db, signaled_comment.reason_id)
        reason_response = ReasonSchemaResponse(
            id=reason.id,
            reason=reason.reason
        )


        event = event_service.get_event_by_id(db, signaled_comment.event_id)
        profile_event = profile_service.get_profile(db, event.profile_id)
        user = user_service.get_user(db, profile_event.user_id)
        role = role_service.get_role_by_id(db, user.role_id)
        role = RoleSchemaResponse(
            id=role.id,
            role=role.role
        )
        user = UserResponse(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            is_planner=user.is_planner,
            role=role,
            account_id=user.account_id
        )
        profile =  ProfileRestrictedSchemaResponse(
            id=profile_event.id,
            first_name=profile_event.first_name,
            last_name=profile_event.last_name,
            photo=profile_event.photo,
            nb_like=profile_event.nb_like,
            email=user.email,
            created_at=profile_event.created_at,
            )

        all_types = []

        for type_ in type_service.get_event_types(db, event.id):
            all_types.append(
                TypeSchemaResponse(
                    id=type_.id,
                    type=type_.type
                )
            )

        event_pictures = []
        for picture in event_picture_service.get_pictures_from_event(db, event.id):
            event_pictures.append(
                EventPictureSchemaResponse(
                    id=picture.id,
                    photo=picture.photo
                )
            )

        event_address = AddressSchemaResponse(
            id=event.address.id,
            city=event.address.city,
            zipcode=event.address.zipcode,
            number=event.address.number,
            street=event.address.street,
            country=event.address.country
        )

        event_schema =  EventSchemaResponse(
            id=event.id,
            title=event.title,
            description=event.description,
            nb_places=event.nb_places,
            price=event.price,
            profile=profile,
            nb_likes=event.nb_likes,
            nb_comments=event.nb_comments,
            date=event.date,
            cloture_billets=event.cloture_billets,
            address=event_address,
            created_at=event.created_at,
            updated_at=event.updated_at,
            types=all_types,
            pictures=event_pictures
        )

        all_signaled_events.append(
            SignaledEventSchemaResponse(
                id=signaled_comment.id,
                event=event_schema,
                reason=reason_response,
                user_id=signaled_by.id,
                created_at=signaled_comment.created_at,
                status=signaled_comment.status
            )
        )

    return SignaledEventListSchemaResponse(
        count=len(all_signaled_events),
        data=all_signaled_events
    )

def get_signaled_events_filters(
    db: Session,
    date: Optional[datetime],
    user_id: Optional[int],
    reason_id: Optional[int],
    event_id: Optional[int],
    status: Optional[int],
    email_user: Optional[str],
    email_event_user: Optional[str],
    offset: int,
    limit: int
) -> SignaledEventListSchemaResponse:
    """
    Retrieves a list of signaled events filtered by various parameters such as date, user ID,
    reason ID, event ID, and status. It also supports filtering by user email and event creator's email.

    Args:
        db (Session): The database session used for querying data.
        date (Optional[datetime]): The date the event was signaled.
        user_id (Optional[int]): The ID of the user who signaled the event.
        reason_id (Optional[int]): The reason the event was signaled.
        event_id (Optional[int]): The ID of the event being signaled.
        status (Optional[int]): The status of the signaled event.
        email_user (Optional[str]): The email of the user who signaled the event.
        email_event_user (Optional[str]): The email of the user who posted the event.
        offset (int): The number of records to skip for pagination.
        limit (int): The maximum number of records to return for pagination.

    Returns:
        SignaledEventListSchemaResponse: A response schema containing the filtered list of signaled events,
        including details about the events, the users who signaled them, and the reasons for signaling.
    """
    signaled_events = signaled_event_service.get_signaled_events_by_filters(
        db,
        date,
        reason_id,
        user_id,
        event_id,
        status,
        email_user,
        email_event_user,
        offset,
        limit
    )

    all_signaled_events = []

    for signaled_comment in signaled_events:
        signaled_by = user_service.get_user(db, signaled_comment.user_id)

        reason = reason_service.get_reason_by_id(db, signaled_comment.reason_id)
        reason_response = ReasonSchemaResponse(
            id=reason.id,
            reason=reason.reason
        )


        #### SEARCH FOR PROFILE THAT POSTED EVENT ######

        event = event_service.get_event_by_id(db, signaled_comment.event_id)
        profile_event = profile_service.get_profile(db, event.profile_id)
        user = user_service.get_user(db, profile_event.user_id)
        role = role_service.get_role_by_id(db, user.role_id)
        role = RoleSchemaResponse(
            id=role.id,
            role=role.role
        )
        user = UserResponse(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            is_planner=user.is_planner,
            role=role,
            account_id=user.account_id
        )
        profile =  ProfileRestrictedSchemaResponse(
            id=profile_event.id,
            first_name=profile_event.first_name,
            last_name=profile_event.last_name,
            photo=profile_event.photo,
            nb_like=profile_event.nb_like,
            email=user.email,
            created_at=profile_event.created_at
        )

        all_types = []

        for type_ in type_service.get_event_types(db, event.id):
            all_types.append(
                TypeSchemaResponse(
                    id=type_.id,
                    type=type_.type
                )
            )

        event_pictures = []
        for picture in event_picture_service.get_pictures_from_event(db, event.id):
            event_pictures.append(
                EventPictureSchemaResponse(
                    id=picture.id,
                    photo=picture.photo
                )
            )

        event_address = AddressSchemaResponse(
            id=event.address.id,
            city=event.address.city,
            zipcode=event.address.zipcode,
            number=event.address.number,
            street=event.address.street,
            country=event.address.country
        )

        event_schema =  EventSchemaResponse(
            id=event.id,
            title=event.title,
            description=event.description,
            nb_places=event.nb_places,
            price=event.price,
            profile=profile,
            nb_likes=event.nb_likes,
            nb_comments=event.nb_comments,
            date=event.date,
            cloture_billets=event.cloture_billets,
            address=event_address,
            created_at=event.created_at,
            updated_at=event.updated_at,
            types=all_types,
            pictures=event_pictures
        )

        all_signaled_events.append(
            SignaledEventSchemaResponse(
                id=signaled_comment.id,
                event=event_schema,
                reason=reason_response,
                user_id=signaled_by.id,
                created_at=signaled_comment.created_at,
                status=signaled_comment.status
            )
            )

    return SignaledEventListSchemaResponse(
        count=len(all_signaled_events),
        data=all_signaled_events
    )

def update_signaled_event_status(db: Session, signaled_event_id: int, status: str) -> SignaledEventSchemaResponse:
    """
    Updates the status of a signaled event and returns the updated information of the event,
    including its details, reasons, and user information.

    Args:
        db (Session): The database session used for querying data.
        signaled_event_id (int): The ID of the signaled event whose status needs to be updated.
        status (str): The new status for the signaled event (e.g., 'resolved', 'pending').

    Returns:
        SignaledEventSchemaResponse: A response schema containing the updated information about
        the signaled event, including event details, the reason for signaling, and the user who signaled it.
    """
    signaled_event = signaled_event_service.update_status_signaled_event(
        db=db,
        id=signaled_event_id,
        status=status
    )

    signaled_by = user_service.get_user(db, signaled_event.user_id)

    reason = reason_service.get_reason_by_id(db, signaled_event.reason_id)
    reason_response = ReasonSchemaResponse(
        id=reason.id,
        reason=reason.reason
    )

    #### SEARCH FOR PROFILE THAT POSTED EVENT ######

    event = event_service.get_event_by_id(db, signaled_event.event_id)
    profile_event = profile_service.get_profile(db, event.profile_id)
    user = user_service.get_user(db, profile_event.user_id)
    role = role_service.get_role_by_id(db, user.role_id)
    role = RoleSchemaResponse(
        id=role.id,
        role=role.role
    )
    user = UserResponse(
        id=user.id,
        email=user.email,
        phone_number=user.phone_number,
        is_planner=user.is_planner,
        role=role,
        account_id=user.account_id
    )
    profile =  ProfileRestrictedSchemaResponse(
        id=profile_event.id,
        first_name=profile_event.first_name,
        last_name=profile_event.last_name,
        photo=profile_event.photo,
        nb_like=profile_event.nb_like,
        email=user.email,
        created_at=profile_event.created_at,
        updated_at=profile_event.updated_at
        )

    all_types = []

    for type_ in type_service.get_event_types(db, event.id):
        all_types.append(
            TypeSchemaResponse(
                id=type_.id,
                type=type_.type
            )
        )

    event_pictures = []
    for picture in event_picture_service.get_pictures_from_event(db, event.id):
        event_pictures.append(
            EventPictureSchemaResponse(
                id=picture.id,
                photo=picture.photo
            )
        )

    event_address = AddressSchemaResponse(
        id=event.address.id,
        city=event.address.city,
        zipcode=event.address.zipcode,
        number=event.address.number,
        street=event.address.street,
        country=event.address.country
    )

    event_schema =  EventSchemaResponse(
        id=event.id,
        title=event.title,
        description=event.description,
        nb_places=event.nb_places,
        price=event.price,
        profile=profile,
        nb_likes=event.nb_likes,
        nb_comments=event.nb_comments,
        date=event.date,
        cloture_billets=event.cloture_billets,
        address=event_address,
        created_at=event.created_at,
        updated_at=event.updated_at,
        types=all_types,
        pictures=event_pictures
    )

    return SignaledEventSchemaResponse(
        id=signaled_event.id,
        event=event_schema,
        reason=reason_response,
        user_id=signaled_by.id,
        created_at=signaled_event.created_at,
        status=signaled_event.status
    )

def delete_signaled_event(db: Session, signaled_event_id: int, current_user: User, ban: bool) -> dict[str, str]:
    """
    Deletes a signaled event from the system, either by banning the event or unsignaling it,
    and logs the action performed by the current user.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): The ID of the signaled event to be deleted or banned.
        current_user (User): The user who is performing the action (ban or unsignal).
        ban (bool): Whether to ban the event (True) or unsignal it (False).

    Returns:
        dict[str, str]: A dictionary with a message indicating the result of the operation.

    Notes:
        - If `ban` is set to True, the event is banned, and a warning-level log is created.
        - If `ban` is set to False, the event is unsignaled, and an info-level log is created.
    """
    moderation_service.delete_signaled_event(db, signaled_event_id, ban, current_user.id)
    if ban:
        action_log_service.create_action_log(
            db,
            current_user.id,
            LogLevelEnum.WARNING,
            ActionEnum.EVENT_BANNED,
            f"Profile {current_user.id} banned signaled event {signaled_event_id} at {datetime.now()} bt {current_user.email}"
        )
    else:
        action_log_service.create_action_log(
            db,
            current_user.id,
            LogLevelEnum.INFO,
            ActionEnum.EVENT_UNSIGNALED,
            f"Profile {current_user.id} unsignaled event {id} at {datetime.now()} by {current_user.email}"
        )
    return {"msg": "deleted"}

def get_signaled_event_by_id(db: Session, signaled_event_id: int) -> SignaledEventSchemaResponse:
    """
    Retrieves a signaled event by its ID, along with detailed information about the event,
    the user who signaled it, the reason for the signal, and the profile of the event poster.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): The ID of the signaled event to retrieve.

    Returns:
        SignaledEventSchemaResponse: A schema response containing the details of the signaled event,
        including the event's profile, reason for being signaled, and the user who signaled it.
    """
    signaled_event = signaled_event_service.get_signaled_event_by_id(db, signaled_event_id)

    signaled_by = user_service.get_user(db, signaled_event.user_id)


    reason = reason_service.get_reason_by_id(db, signaled_event.reason_id)
    reason_response = ReasonSchemaResponse(
        id=reason.id,
        reason=reason.reason
    )

    #### SEARCH FOR PROFILE THAT POSTED EVENT ######

    event = event_service.get_event_by_id(db, signaled_event.event_id)
    profile_event = profile_service.get_profile(db, event.profile_id)
    user = user_service.get_user(db, profile_event.user_id)

    profile =  ProfileRestrictedSchemaResponse(
        id=profile_event.id,
        first_name=profile_event.first_name,
        last_name=profile_event.last_name,
        photo=profile_event.photo,
        nb_like=profile_event.nb_like,
        email=user.email,
        created_at=profile_event.created_at
    )

    all_types = []

    for type_ in type_service.get_event_types(db, event.id):
        all_types.append(
            TypeSchemaResponse(
                id=type_.id,
                type=type_.type
            )
        )

    event_pictures = []
    for picture in event_picture_service.get_pictures_from_event(db, event.id):
        event_pictures.append(
            EventPictureSchemaResponse(
                id=picture.id,
                photo=picture.photo
            )
        )

    event_address = AddressSchemaResponse(
        id=event.address.id,
        city=event.address.city,
        zipcode=event.address.zipcode,
        number=event.address.number,
        street=event.address.street,
        country=event.address.country
    )

    event_schema =  EventSchemaResponse(
        id=event.id,
        title=event.title,
        description=event.description,
        nb_places=event.nb_places,
        price=event.price,
        profile=profile,
        nb_likes=event.nb_likes,
        nb_comments=event.nb_comments,
        date=event.date,
        cloture_billets=event.cloture_billets,
        address=event_address,
        created_at=event.created_at,
        updated_at=event.updated_at,
        types=all_types,
        pictures=event_pictures
    )

    return SignaledEventSchemaResponse(
        id=signaled_event.id,
        event=event_schema,
        reason=reason_response,
        user_id=signaled_by.id,
        created_at=signaled_event.created_at,
        status=signaled_event.status
    )
