"""
This file contains the controller related to events
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from models.user_model import User
from schemas.response_schemas.profile_schema_response import ProfileRestrictedSchemaResponse
from services import (
    action_log_service,
    address_service,
    event_picture_service,
    event_service,
    moderation_service,
    profile_service,
    user_service
)
from schemas.request_schemas.event_schema import EventSchema
from schemas.response_schemas.event_schema_response import EventSchemaResponse, EventListSchemaResponse
from schemas.response_schemas.type_schema_response import TypeSchemaResponse
from schemas.response_schemas.address_schema_response import AddressSchemaResponse
from schemas.request_schemas.event_picture_schema import EventPictureSchema
from schemas.response_schemas.event_picture_schema_response import EventPictureSchemaResponse
from models.event_picture_model import EventPicture
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum
from errors import NoStripeAccountError, EventNotFound, ProfileNotFound


def create_event(db: Session, event: EventSchema, current_user: User) -> EventSchemaResponse:
    """
    Creates a new event, associates it with the current user, and handles address and pictures.

    Args:
        db (Session): The database session used to interact with the database.
        event (EventSchema): The schema containing the event data, including title, description, and address.
        current_user (User): The user who is creating the event.

    Returns:
        EventSchemaResponse: The response schema containing the newly created event information.

    Raises:
        NoStripeAccountError: If the event has a price greater than 0 and the user does not have a Stripe account.
    """
    if event.price > 0.0 and not current_user.account_id:
        raise NoStripeAccountError(status_code=403, detail="Please create a stripe account before posting an event")

    profile = profile_service.get_profile(
        db,
        current_user.id
    )
    address = address_service.create_address(
        db,
        event.address.city,
        event.address.zipcode,
        event.address.number,
        event.address.street,
        event.address.country
    )

    new_event = event_service.create_event(
        db,
        event.title,
        event.description,
        event.nb_places,
        event.price,
        profile.id,
        event.date,
        event.cloture_billets,
        event.types.types,
        address.id
    )

    if current_user.is_planner is False:
        user_service.toggle_is_planner(db, current_user.id)

    event_pictures = []
    for picture in event.pictures:
        pic = event_picture_service.create_event_picture(
            db,
            new_event.id,
            picture.photo
        )
        event_pictures.append(
            EventPictureSchemaResponse(
                id=pic.id,
                photo=pic.photo
            )
        )

    profile =  ProfileRestrictedSchemaResponse(
        id=profile.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        photo=profile.photo,
        nb_like=profile.nb_like,
        email=current_user.email,
        created_at=profile.created_at,
        )

    all_types = []

    for type_ in new_event.types:
        all_types.append(
            TypeSchemaResponse(
                id=type_.id,
                type=type_.type
            )
        )
    event_address = AddressSchemaResponse(
        id=new_event.address.id,
        city=new_event.address.city,
        zipcode=new_event.address.zipcode,
        number=new_event.address.number,
        street=new_event.address.street,
        country=new_event.address.country
    )

    action_log_service.create_action_log(
        db,
        current_user.id,
        LogLevelEnum.INFO,
        ActionEnum.EVENT_CREATED,
        f"Event {new_event.id} created at {new_event.created_at} created by {current_user.email}"
    )

    return EventSchemaResponse(
        id=new_event.id,
        title=new_event.title,
        description=new_event.description,
        nb_places=new_event.nb_places,
        price=new_event.price,
        profile=profile,
        nb_likes=new_event.nb_likes,
        nb_comments=new_event.nb_comments,
        date=new_event.date,
        cloture_billets=new_event.cloture_billets,
        address=event_address,
        created_at=new_event.created_at,
        updated_at=new_event.updated_at,
        types=all_types,
        pictures=event_pictures
    )


def get_event_by_id(db: Session, event_id: int) -> EventSchemaResponse:
    """
    Retrieves an event by its ID, along with related information including the profile of the user who created it,
    event types, event pictures, and the event address.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): The ID of the event to retrieve.

    Returns:
        EventSchemaResponse: The detailed event information, including the profile of the creator,
                              event types, event pictures, and event address.

    Raises:
        EventNotFound: If no event is found with the provided ID.
        ProfileNotFound: If no profile is found for the user who created the event.
    """
    event = event_service.get_event_by_id(db, event_id)

    if not event:
        raise EventNotFound(status_code=404, detail="L'event n'a pas été trouvé")

    profile = profile_service.get_profile(db, event.profile_id)

    if not profile:
        raise ProfileNotFound(status_code=404, detail="Le profil n'a pas été trouvé")

    user = user_service.get_user(db, profile.user_id)

    profile =  ProfileRestrictedSchemaResponse(
        id=profile.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        photo=profile.photo,
        nb_like=profile.nb_like,
        email=user.email,
        created_at=profile.created_at,
        )

    all_types = []

    for type_ in event.types:
        all_types.append(
            TypeSchemaResponse(
                id=type_.id,
                type=type_.type
            )
        )

    event_pictures = []
    for picture in event.pictures:
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

    return EventSchemaResponse(
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


def get_events(
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
) -> EventListSchemaResponse:
    """
    Retrieves a list of events based on various filters, including date range, type, location, and search query.
    The events are returned with detailed information, such as the profile of the user who created the event,
    event types, event pictures, and event address.

    Args:
        db (Session): The database session used to interact with the database.
        date_avant (Optional[datetime]): The end date for the event search.
        date_apres (Optional[datetime]): The start date for the event search.
        type_ids (Optional[list[int]]): A list of event type IDs to filter by.
        profile_id (Optional[int]): The profile ID to filter events by.
        country (Optional[str]): The country to filter events by.
        city (Optional[str]): The city to filter events by.
        popularity (Optional[bool]): Whether to filter by event popularity.
        recent (Optional[bool]): Whether to filter by recent events.
        nb_places (Optional[int]): The number of available places to filter by.
        search (Optional[str]): The search keyword to filter events by title or description.
        offset (int): The starting index for pagination.
        limit (int): The maximum number of events to retrieve.

    Returns:
        EventListSchemaResponse: A response containing the list of events matching the filter criteria,
                                 along with the total count of events.

    Raises:
        ProfileNotFound: If the profile associated with an event cannot be found.
    """
    events = event_service.get_events_filters(
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

    all_events = []

    for event in events:
        profile = profile_service.get_profile(db, event.profile_id)

        if not profile:
            raise ProfileNotFound(status_code=404, detail="Le profil n'a pas été trouvé")

        user = user_service.get_user(db, profile.user_id)

        profile_schema =  ProfileRestrictedSchemaResponse(
            id=profile.id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            photo=profile.photo,
            nb_like=profile.nb_like,
            email=user.email,
            created_at=profile.created_at,
            )

        all_types = []

        for type_ in event.types:
            all_types.append(
                TypeSchemaResponse(
                    id=type_.id,
                    type=type_.type
                )
            )

        event_pictures = []
        for picture in event.pictures:
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
        all_events.append(
            EventSchemaResponse(
                id=event.id,
                title=event.title,
                description=event.description,
                nb_places=event.nb_places,
                price=event.price,
                profile=profile_schema,
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
        )
    total_events = event_service.get_count_total_events(
        db,
        date_avant,
        date_apres,
        type_ids,
        profile_id,
        country,
        city,
        search
    )

    return EventListSchemaResponse(
        count=len(all_events),
        total=total_events,
        data=all_events
    )


def update_event(db: Session, event_id: int, event: EventSchema) -> EventSchemaResponse:
    """
    Updates an existing event in the database with the provided details.

    This function updates the event title, description, number of places, price,
    event date, and types. It also updates the event's address and its associated pictures.
    After updating the event, an action log is created to track the update.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): The ID of the event to update.
        event (EventSchema): The updated event details.

    Returns:
        EventSchemaResponse: A response containing the updated event information, including
                              the profile of the event creator, event types, pictures, and address.

    Raises:
        Exception: If the event or any related entities cannot be found or updated.
    """
    event_ = event_service.update_event(
        db,
        event_id,
        event.title,
        event.description,
        event.nb_places,
        event.price,
        event.date,
        event.cloture_billets,
        event.types.types
    )
    address = address_service.update_address(
        db,
        event_.address_id,
        event.address.city,
        event.address.zipcode,
        event.address.number,
        event.address.street,
        event.address.country
    )
    profile = profile_service.get_profile(db, event_.profile_id)
    user = user_service.get_user(db, profile.user_id)
    update_event_pictures(db, event_.pictures, event.pictures, event_.id)

    profile =  ProfileRestrictedSchemaResponse(
        id=profile.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        photo=profile.photo,
        nb_like=profile.nb_like,
        email=user.email,
        created_at=profile.created_at,
        )

    all_types = []

    for type_ in event_.types:
        all_types.append(
            TypeSchemaResponse(
                id=type_.id,
                type=type_.type
            )
        )

    all_pics = []
    for picture in event_.pictures:
        all_pics.append(
            EventPictureSchemaResponse(
                id=picture.id,
                photo=picture.photo
            )
        )
    event_address = AddressSchemaResponse(
        id=address.id,
        city=address.city,
        zipcode=address.zipcode,
        number=address.number,
        street=address.street,
        country=address.country
    )

    action_log_service.create_action_log(
        db,
        user.id,
        LogLevelEnum.INFO,
        ActionEnum.EVENT_UPDATED,
        f"Event {event_.id} updated at {event_.updated_at} by {user.email}"
    )

    return EventSchemaResponse(
        id=event_.id,
        title=event_.title,
        description=event_.description,
        nb_places=event_.nb_places,
        price=event_.price,
        profile=profile,
        nb_likes=event_.nb_likes,
        nb_comments=event_.nb_comments,
        date=event_.date,
        cloture_billets=event_.cloture_billets,
        address=event_address,
        created_at=event_.created_at,
        updated_at=event_.updated_at,
        types=all_types,
        pictures=all_pics
    )


def delete_event(db: Session, event_id: int, current_user: User) -> dict[str, str]:
    """
    Deletes an event from the database based on its ID.

    This function retrieves the event by its ID, ensures that the user has the right permissions
    to delete the event, and then deletes the event from the database. An action log is created
    to track the deletion of the event.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): The ID of the event to delete.
        current_user (User): The user attempting to delete the event.

    Returns:
        dict[str, str]: A dictionary containing a message indicating that the event has been deleted.

    """
    event = event_service.get_event_by_id(db, event_id)

    # ⚠️ user.id == profile.id by design
    user = user_service.get_user(db, event.profile_id)

    moderation_service.delete_event(db, event_id, current_user.id)

    action_log_service.create_action_log(
        db,
        user.id,
        LogLevelEnum.INFO,
        ActionEnum.EVENT_DELETED,
        f"Event {event.id} deleted at {event.created_at} by {user.email}"
    )
    return JSONResponse(content={"msg": "event supprimé"})


def update_event_pictures(
    db: Session,
    event_pictures: list[EventPicture],
    update_pictures: list[EventPictureSchema],
    event_id: int
) -> None:
    """
    Updates the pictures of an event by comparing existing pictures with the updated ones.

    This function compares the event's current pictures with the list of updated pictures.
    It adds new pictures, removes deleted ones, and ensures the event's pictures list is up to date.

    Args:
        db (Session): The database session used to interact with the database.
        event_pictures (list[EventPicture]): A list of the current pictures associated with the event.
        update_pictures (list[EventPictureSchema]): A list of updated picture schemas containing the new pictures.
        event_id (int): The ID of the event for which the pictures need to be updated.

    Returns:
        None
    """
    event_pictures_set = {pic.photo for pic in event_pictures}
    update_pictures_set = {pic.photo for pic in update_pictures}

    pics_to_remove = event_pictures_set - update_pictures_set
    pics_to_add = update_pictures_set - event_pictures_set

    event_picture_service.delete_pictures(db, list(pics_to_remove))
    event_picture_service.add_picture_to_event(db, list(pics_to_add), event_id)


def get_events_by_profile(
    db: Session,
    profile_id: int,
    offset: int,
    limit: int
) -> EventListSchemaResponse:
    """
    Récupère les événements associés à un profil spécifique avec une pagination.

    Cette fonction récupère tous les événements associés au profil dont l'ID est fourni.
    Les événements sont paginés selon les paramètres `offset` et `limit`.

    Args:
        db (Session): La session de la base de données utilisée pour effectuer les opérations.
        profile_id (int): L'ID du profil pour lequel les événements doivent être récupérés.
        offset (int): Le nombre d'événements à ignorer avant de commencer à retourner les résultats.
        limit (int): Le nombre d'événements à récupérer par page.

    Returns:
        EventListSchemaResponse: Un objet contenant la liste des événements récupérés et le nombre total d'événements.
    """
    events = event_service.get_events_by_profile(
        db,
        profile_id,
        offset,
        limit
    )

    all_events = []

    for event in events:
        profile = profile_service.get_profile(db, event.profile_id)
        user = user_service.get_user(db, profile.user_id)

        profile =  ProfileRestrictedSchemaResponse(
            id=profile.id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            photo=profile.photo,
            nb_like=profile.nb_like,
            email=user.email,
            created_at=profile.created_at,
            )

        all_types = []

        for type_ in event.types:
            all_types.append(
                TypeSchemaResponse(
                    id=type_.id,
                    type=type_.type
                )
            )

        event_pictures = []
        for picture in event.pictures:
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
        all_events.append(
            EventSchemaResponse(
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
        )

    total_events = event_service.get_count_total_events(
        db=db,
        profile_id=profile_id,
    )
    return EventListSchemaResponse(
        total=total_events,
        count=len(all_events),
        data=all_events
    )
