"""
This file contains the controller related to comments
"""
from sqlalchemy.orm import Session
from errors import CommentNotFound, ProfileNotFound, EventNotFound
from schemas.response_schemas.profile_schema_response import ProfileRestrictedSchemaResponse
from services import (
    comment_service,
    event_service,
    moderation_service,
    profile_service,
    user_service
)
from schemas.request_schemas.comment_schema import CommentSchema
from schemas.response_schemas.comment_schema_response import CommentSchemaResponse, CommentListSchemaResponse


def comment_event(db: Session, comment: CommentSchema, profile_id: int) -> CommentSchemaResponse:
    """
    Allows a user to comment on an event.

    Args:
        db (Session): The database session used to interact with the database.
        comment (CommentSchema): The schema containing the comment content and event information.
        profile_id (int): The profile ID of the user commenting.

    Returns:
        CommentSchemaResponse: The response schema containing the new comment information, including the user profile and event details.

    Raises:
        ProfileNotFound: If the profile corresponding to `profile_id` is not found.
        EventNotFound: If the event corresponding to `comment.event_id` is not found.
    """
    new_comment = comment_service.comment_event(db, profile_id=profile_id, event_id=comment.event_id, content=comment.content)

    try:
        profile = profile_service.get_profile(db, profile_id)
        if not profile:
            raise ProfileNotFound(status_code=404, detail="Le profil n'a pas été trouvé")

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

        event = event_service.get_event_by_id(db, comment.event_id)
        if not event:
            raise EventNotFound(status_code=404, detail="Le profil n'a pas été trouvé")

        return CommentSchemaResponse(
            id=new_comment.id,
            profile=profile_schema,
            event_id=event.id,
            content=new_comment.content,
            created_at=new_comment.created_at
        )
    except (ProfileNotFound, EventNotFound) as e:
        moderation_service.delete_comment(db, new_comment.id, profile_id)
        raise e


def get_comments_from_event(db: Session, event_id: int, offset: int, limit: int) -> CommentListSchemaResponse:
    """
    Retrieves a list of comments for a specific event, with pagination.

    Args:
        db (Session): The database session used to interact with the database.
        event_id (int): The event ID for which the comments are being fetched.
        offset (int): The starting point for pagination.
        limit (int): The maximum number of results to return.

    Returns:
        CommentListSchemaResponse: A response schema containing the list of comments and the count.

    Raises:
        ProfileNotFound: If the profile associated with the comment is not found.
        EventNotFound: If the event corresponding to the comment is not found.
    """
    comments = comment_service.get_comment_by_event(db, event_id, offset, limit)

    all_comments = []
    for comment in comments:
        profile = profile_service.get_profile(db, comment.profile_id)

        if not profile:
            raise ProfileNotFound(status_code=404, detail="Le profil n'a pas été trouvé")

        user = user_service.get_user(db, profile.user_id)

        profile_schema = ProfileRestrictedSchemaResponse(
            id=profile.id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            photo=profile.photo,
            nb_like=profile.nb_like,
            email=user.email,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )

        event = event_service.get_event_by_id(db, comment.event_id)
        if not event:
            raise EventNotFound(status_code=404, detail="L'event n'a pas été trouvé")

        all_comments.append(CommentSchemaResponse(
            id=comment.id,
            profile=profile_schema,
            event_id=event.id,
            content=comment.content,
            created_at=comment.created_at
        ))

    return CommentListSchemaResponse(
        count=len(all_comments),
        data=all_comments
    )


def get_comments(db: Session, offset: int, limit: int) -> CommentListSchemaResponse:
    """
    Retrieves a list of all comments, with pagination.

    Args:
        db (Session): The database session used to interact with the database.
        offset (int): The starting point for pagination.
        limit (int): The maximum number of results to return.

    Returns:
        CommentListSchemaResponse: A response schema containing the list of comments and the count.

    Raises:
        ProfileNotFound: If the profile associated with the comment is not found.
        EventNotFound: If the event corresponding to the comment is not found.
    """
    comments = comment_service.get_all_comments(db, offset, limit)

    all_comments = []
    for comment in comments:
        profile = profile_service.get_profile(db, comment.profile_id)
        if not profile:
            raise ProfileNotFound(status_code=404, detail="Le profil n'a pas été trouvé")

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

        event = event_service.get_event_by_id(db, comment.event_id)
        if not event:
            raise EventNotFound(status_code=404, detail="L'event n'a pas été trouvé")

        all_comments.append(CommentSchemaResponse(
            id=comment.id,
            profile=profile_schema,
            event_id=event.id,
            content=comment.content,
            created_at=comment.created_at
        ))

    return CommentListSchemaResponse(
        count=len(all_comments),
        data=all_comments
    )


def delete_comment(db: Session, comment_id: int, current_user_id: int) -> dict[str, str]:
    """
    Deletes a comment by its ID.

    Args:
        db (Session): The database session used to interact with the database.
        comment_id (int): The ID of the comment to be deleted.
        current_user_id (int): The ID of the current user performing the delete operation.

    Returns:
        dict[str, str]: A confirmation message indicating the comment was deleted.

    Raises:
        CommentNotFound: If no comment is found with the provided `comment_id`.
    """
    if not get_comment_by_id(db, comment_id):
        raise CommentNotFound(status_code=404, detail="Le commentaire n'a pas été trouvé")
    moderation_service.delete_comment(db, comment_id, current_user_id)
    return {"msg": "commentaire supprimé"}


def get_comment_by_id(db: Session, comment_id: int) -> CommentSchemaResponse:
    """
    Retrieves a comment by its ID.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): The ID of the comment to be fetched.

    Returns:
        CommentSchemaResponse: A response schema containing the comment details.

    Raises:
        CommentNotFound: If no comment is found with the provided `id`.
    """
    comment = comment_service.get_comment_by_id(db, comment_id)

    if not comment:
        raise CommentNotFound(status_code=404, detail="Le comment n'a pas été trouvé")
    profile = profile_service.get_profile(db, comment.profile_id)

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

    event = event_service.get_event_by_id(db, comment.event_id)

    return CommentSchemaResponse(
        id=comment.id,
        profile=profile_schema,
        event_id=event.id,
        content=comment.content,
        created_at=comment.created_at
    )


def get_comments_from_profile(db: Session, profile_id: int, offset: int, limit: int) -> CommentListSchemaResponse:
    """
    Retrieves a list of comments for a specific profile, with pagination.

    Args:
        db (Session): The database session used to interact with the database.
        profile_id (int): The profile ID for which the comments are being fetched.
        offset (int): The starting point for pagination.
        limit (int): The maximum number of results to return.

    Returns:
        CommentListSchemaResponse: A response schema containing the list of comments and the count.

    Raises:
        ProfileNotFound: If the profile corresponding to `profile_id` is not found.
        EventNotFound: If the event corresponding to a comment is not found.
    """
    comments = comment_service.get_comment_from_profile(db, profile_id, offset, limit)

    all_comments = []
    for comment in comments:
        profile = profile_service.get_profile(db, comment.profile_id)
        if not profile:
            raise ProfileNotFound(status_code=404, detail="Le profil n'a pas été trouvé")

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

        #### SEARCH FOR PROFILE THAT POSTED EVENT ######

        event = event_service.get_event_by_id(db, comment.event_id)
        if not event:
            raise EventNotFound(status_code=404, detail="L'event n'a pas été trouvé")

        all_comments.append(CommentSchemaResponse(
            id=comment.id,
            profile=profile_schema,
            event_id=event.id,
            content=comment.content,
            created_at=comment.created_at
        ))

    return CommentListSchemaResponse(
        count=len(all_comments),
        data=all_comments
    )
