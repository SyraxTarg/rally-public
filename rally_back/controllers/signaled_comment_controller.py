"""
This file contains the controller related to signaled comments
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from schemas.request_schemas.signaled_comment_schema import SignaledCommentByCurrentUserSchema
from schemas.response_schemas.reason_schema_response import ReasonSchemaResponse
from schemas.response_schemas.signaled_comment_schema_response import SignaledCommentSchemaResponse, SignaledCommentListSchemaResponse
from schemas.response_schemas.profile_schema_response import ProfileRestrictedSchemaResponse
from schemas.response_schemas.comment_schema_response import CommentSchemaResponse
from services import (
    action_log_service,
    comment_service,
    event_service,
    moderation_service,
    profile_service,
    reason_service,
    signaled_comment_service,
    user_service
)
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum
from models.user_model import User


def create_signaled_comment_by_current_user(
    db: Session,
    signaled_comment: SignaledCommentByCurrentUserSchema,
    current_user: User
) -> bool:
    """
    Allows a user to signal a comment, indicating that it violates community guidelines, by providing the comment ID
    and the reason for reporting. This action also logs the event for auditing purposes.

    Args:
        db (Session): The database session used for interacting with the database.
        signaled_comment (SignaledCommentByCurrentUserSchema): The schema containing the comment ID and the reason for signaling.
        current_user (User): The user who is signaling the comment.

    Returns:
        bool: Returns True if the signaled comment was successfully created, otherwise False.
    """
    action_log_service.create_action_log(
        db,
        current_user.id,
        LogLevelEnum.INFO,
        ActionEnum.COMMENT_SIGNALED,
        f"Profile {current_user.id} signaled comment {signaled_comment.comment_id} at {datetime.now()} by {current_user.email}"
    )

    return signaled_comment_service.create_signaled_comment(
        db=db,
        comment_id=signaled_comment.comment_id,
        user_id=current_user.id,
        reason_id=signaled_comment.reason_id
    )


def get_signaled_comments_filters(
    db: Session,
    date: Optional[datetime],
    user_id: Optional[int],
    reason_id: Optional[int],
    comment_id: Optional[int],
    status: Optional[str],
    email_user: Optional[str],
    email_comment_user: Optional[str],
    offset: int,
    limit: int
) -> SignaledCommentListSchemaResponse:
    """
    Retrieves a list of signaled comments based on various filter criteria such as the date of signaling,
    user ID, reason ID, comment ID, status, and email information. This function processes and formats
    the results for further use.

    Args:
        db (Session): The database session used to query the database.
        date (Optional[datetime]): The date when the comment was signaled.
        user_id (Optional[int]): The ID of the user who signaled the comment.
        reason_id (Optional[int]): The reason ID for signaling the comment.
        comment_id (Optional[int]): The ID of the comment being signaled.
        status (Optional[str]): The status of the signaled comment (e.g., "pending", "resolved").
        email_user (Optional[str]): The email address of the user who signaled the comment.
        email_comment_user (Optional[str]): The email address of the user who made the commented content.
        offset (int): The number of records to skip (for pagination).
        limit (int): The maximum number of records to return.

    Returns:
        SignaledCommentListSchemaResponse: A response schema containing the count and list of signaled comments.
    """
    signaled_comments = signaled_comment_service.get_signaled_comments_by_filters(
        db,
        date,
        reason_id,
        user_id,
        comment_id,
        status,
        email_user,
        email_comment_user,
        offset,
        limit
    )
    
    total = signaled_comment_service.get_signaled_comments_by_filters_total_count(
        db,
        date,
        reason_id,
        user_id,
        comment_id,
        status,
        email_user,
        email_comment_user
    )

    all_signaled_comments = []

    for signaled_comment in signaled_comments:
        signaled_by = user_service.get_user(db, signaled_comment.user_id)

        reason = reason_service.get_reason_by_id(db, signaled_comment.reason_id)
        reason_response = ReasonSchemaResponse(
            id=reason.id,
            reason=reason.reason
        )

        comment = comment_service.get_comment_by_id(db, signaled_comment.comment_id)
        if not comment:
            raise ValueError("comment not found")

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

        comment_response = CommentSchemaResponse(
            id=comment.id,
            profile=profile_schema,
            event_id=event.id,
            content=comment.content,
            created_at=comment.created_at
        )

        all_signaled_comments.append(
            SignaledCommentSchemaResponse(
                id=signaled_comment.id,
                comment=comment_response,
                reason=reason_response,
                user_id=signaled_by.id,
                created_at=signaled_comment.created_at,
                status=signaled_comment.status
            )
        )

    return SignaledCommentListSchemaResponse(
        count=len(all_signaled_comments),
        total=total,
        data=all_signaled_comments
    )


def update_signaled_comment_status(db: Session, signaled_comment_id: int, status: str) -> SignaledCommentSchemaResponse:
    """
    Updates the status of a signaled comment and returns the updated signaled comment data.

    Args:
        db (Session): The database session used to query and update the database.
        signaled_comment_id (int): The ID of the signaled comment to update.
        status (str): The new status of the signaled comment (e.g., 'resolved', 'pending').

    Returns:
        SignaledCommentSchemaResponse: The response schema containing the updated signaled comment details,
        including the associated comment, reason for signaling, user information, and updated status.
    """
    signaled_comment = signaled_comment_service.update_status_signaled_comment(
        db=db,
        id=signaled_comment_id,
        status=status
    )

    signaled_by = user_service.get_user(db, signaled_comment.user_id)

    reason = reason_service.get_reason_by_id(db, signaled_comment.reason_id)
    reason_response = ReasonSchemaResponse(
        id=reason.id,
        reason=reason.reason
    )

    comment = comment_service.get_comment_by_id(db, signaled_comment.comment_id)
    if not comment:
        raise ValueError("comment not found")

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

    comment_response = CommentSchemaResponse(
        id=comment.id,
        profile=profile_schema,
        event_id=event.id,
        content=comment.content
    )

    return SignaledCommentSchemaResponse(
        id=signaled_comment.id,
        comment=comment_response,
        reason=reason_response,
        user_id=signaled_by.id,
        created_at=signaled_comment.created_at,
        status=signaled_comment.status
    )


def delete_signaled_comment(db: Session, signaled_comment_id: int, ban: bool, current_user: User) -> dict[str, str]:
    """
    Deletes a signaled comment and optionally bans the user if the comment is flagged for inappropriate content.
    Creates an action log based on whether the comment was banned or the signalment was removed.

    Args:
        db (Session): The database session used for querying and updating the database.
        signaled_comment_id (int): The ID of the signaled comment to delete.
        ban (bool): A flag indicating whether the comment is to be banned. If True, the user who posted the comment
                    will be banned.
        current_user (User): The current logged-in user performing the deletion or banning action.

    Returns:
        dict[str, str]: A dictionary with a confirmation message indicating that the comment has been deleted.
    """
    moderation_service.delete_signaled_comment(db, signaled_comment_id, ban, current_user.id)
    if ban:
        action_log_service.create_action_log(
            db,
            current_user.id,
            LogLevelEnum.WARNING,
            ActionEnum.COMMENT_BANNED,
            f"Admin {current_user.id} accepted signaled comment {id} by {current_user.email}"
        )
    else:
        action_log_service.create_action_log(
            db,
            current_user.id,
            LogLevelEnum.INFO,
            ActionEnum.COMMENT_UNSIGNALED,
            f"Admin {current_user.id} removed comment signalment {id} by {current_user.email}"
        )
    return {"msg": "supprimé"}