"""
This file contains the controller related to likes
"""
from sqlalchemy.orm import Session
from schemas.response_schemas.profile_schema_response import ProfileRestrictedSchemaResponse
from services import (
    event_service,
    like_service,
    profile_service,
    user_service
)
from schemas.response_schemas.like_schema_response import LikeSchemaresponseSchemas,  LikeListSchemaresponseSchemas, IsLikedResponseSchema


def unlike_event(db: Session, profile_id: int, event_id: int) -> dict[str, str]:
    """
    Removes a "like" from an event by a specific profile.

    This function removes a "like" from an event for a given profile.
    It performs the action in the database and returns a confirmation message.

    Args:
        db (Session): The database session used to perform the operation.
        profile_id (int): The ID of the profile removing the "like".
        event_id (int): The ID of the event from which the "like" is removed.

    Returns:
        dict[str, str]: A dictionary containing a confirmation message of the action.
    """
    like_service.unlike_event(db, profile_id, event_id)
    return {"msg": "like removed"}

def get_likes(db: Session, offset: int, limit: int)  ->  LikeListSchemaresponseSchemas:
    """
    Retrieves a list of "likes" from the database with pagination.

    This function fetches all likes within the given offset and limit. It gathers the profile and event
    details for each like, and returns them in a structured response.

    Args:
        db (Session): The database session used to perform the operation.
        offset (int): The number of items to skip before starting to collect results.
        limit (int): The maximum number of items to return in the response.

    Returns:
        LikeListSchemaResponseSchemas: A structured response containing the count and list of likes.
            - count (int): The total number of likes retrieved.
            - data (list): A list of likes, each including profile and event details.
    """
    likes = like_service.get_likes(db, offset, limit)

    all_likes = []

    for like in likes:
        profile = profile_service.get_profile(db, like.profile_id)

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

        event = event_service.get_event_by_id(db, like.event_id)

        all_likes.append(LikeSchemaresponseSchemas(
            id=like.id,
            profile=profile_schema,
            event_id=event.id
        ))

    return  LikeListSchemaresponseSchemas(
        count=len(all_likes),
        data=all_likes
    )

def like_event_current_user(db: Session, profile_id: int, event_id: int) -> LikeSchemaresponseSchemas:
    """
    Allows a user to like an event.

    This function creates a new like for a given event by a specific profile, then returns the details
    of the created like along with the profile and event information.

    Args:
        db (Session): The database session used to perform the operation.
        profile_id (int): The ID of the profile liking the event.
        event_id (int): The ID of the event being liked.

    Returns:
        LikeSchemaResponseSchemas: A structured response containing the created like's details.
            - id (int): The ID of the newly created like.
            - profile (ProfileRestrictedSchemaResponse): Profile details of the user who liked the event.
            - event (int): The ID of the event that was liked.
    """
    new_like = like_service.like_event(db, profile_id, event_id)

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

    event = event_service.get_event_by_id(db, event_id)

    return LikeSchemaresponseSchemas(
        id=new_like.id,
        profile=profile_schema,
        event_id=event.id
    )

def is_event_liked_by_current(db: Session, event_id: int, current_user_id: int) -> bool:
    """
    Checks if the current user has liked a specific event.

    This function queries the database to determine if the current user has already liked the given event.

    Args:
        db (Session): The database session used to perform the operation.
        event_id (int): The ID of the event to check.
        current_user_id (int): The ID of the current user.

    Returns:
        bool: True if the event has been liked by the current user, False otherwise.
    """
    like = like_service.get_like(db, current_user_id, event_id)

    if not like:
        return IsLikedResponseSchema(is_liked=False)

    return IsLikedResponseSchema(is_liked=True)
