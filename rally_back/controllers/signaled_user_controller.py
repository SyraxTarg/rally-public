"""
This file contains the controller related to signaled signaled users
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from schemas.request_schemas.signaled_user_schema import SignaledUserCurrentUSerSchema
from schemas.response_schemas.reason_schema_response import ReasonSchemaResponse
from schemas.response_schemas.signaled_user_schema_response import (
    SignaledUserSchemaResponse,
    SignaledUserListSchemaResponse
)
from services import (
    action_log_service,
    moderation_service,
    reason_service,
    signaled_user_service,
    user_service
)
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum
from models.user_model import User

def delete_signaled_user(db: Session, signaled_user_id: int, current_user: User, ban: bool) -> dict[str, str]:
    """
    Deletes a signaled user, either banning or unbanning them, and logs the action performed
    by the current user.

    Args:
        db (Session): The database session used to interact with the database.
        signaled_user_id (int): The ID of the user being deleted or banned.
        current_user (User): The current user performing the action.
        ban (bool): Flag indicating whether the user is being banned (True) or unbanned (False).

    Returns:
        dict: A dictionary containing a message confirming the deletion, e.g. `{"msg": "delete"}`.
    """
    moderation_service.delete_signaled_user(db, signaled_user_id, ban, current_user.id)
    if ban:
        action_log_service.create_action_log(
            db,
            current_user.id,
            LogLevelEnum.WARNING,
            ActionEnum.USER_BANNED,
            f"Profile {current_user.id} banned user {signaled_user_id} at {datetime.now()} by {current_user.email}"
        )
    else:
        action_log_service.create_action_log(
            db,
            current_user.id,
            LogLevelEnum.INFO,
            ActionEnum.USER_UNSIGNALED,
            f"Profile {current_user.id} unbanned user {id} at {datetime.now()} by {current_user.email}"
        )

    return {"msg": "delete"}

def update_status_signaled_user(db: Session, signaled_user_id: int, status: str) -> SignaledUserSchemaResponse:
    """
    Updates the status of a signaled user and returns a response schema with the updated details.

    This function interacts with the signaled user service to update the status of a signaled user.
    It also fetches the details of the user who was signaled, the user who reported the signal,
    and the reason for the signal.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): The ID of the signaled user whose status is to be updated.
        status (str): The new status for the signaled user (e.g., "banned", "unbanned", etc.).

    Returns:
        SignaledUserSchemaResponse: A response schema containing the updated details of the signaled user,
        including information such as the user's ID, the ID of the user who signaled them, the reason for the signal,
        and the updated status.
    """
    signaled_user = signaled_user_service.update_status_signaled_user(db, signaled_user_id, status)
    user = user_service.get_user(db, signaled_user.user_signaled_id)

    signaled_by = user_service.get_user(db, signaled_user.user_id)

    reason = reason_service.get_reason_by_id(db, signaled_user.reason_id)

    return SignaledUserSchemaResponse(
        id=signaled_user.id,
        user_signaled_id=user.id,
        user_signaled_email=user.email,
        reason=ReasonSchemaResponse(
            id=reason.id,
            reason=reason.reason
        ),
        signaled_by_id=signaled_by.id,
        signaled_by_email=signaled_by.email,
        created_at=signaled_user.created_at,
        status=signaled_user.status
    )

def get_signaled_user_by_filters(
    db: Session,
    date: Optional[datetime],
    user_id: Optional[int],
    reason_id: Optional[int],
    signaled_user_id: Optional[int],
    status: Optional[str],
    email_user: Optional[str],
    email_signaled_user: Optional[str],
    offset: int,
    limit: int
) -> SignaledUserListSchemaResponse:
    """
    Retrieves a list of signaled users filtered by various optional criteria, such as date, user ID,
    reason, status, and email addresses.

    Args:
        db (Session): The database session used to interact with the database.
        date (Optional[datetime]): Optional filter for the date the signal was created.
        user_id (Optional[int]): Optional filter for the ID of the user who signaled the user.
        reason_id (Optional[int]): Optional filter for the ID of the reason for the signal.
        signaled_user_id (Optional[int]): Optional filter for the ID of the user who was signaled.
        status (Optional[str]): Optional filter for the status of the signal (e.g., "banned", "active").
        email_user (Optional[str]): Optional filter for the email of the user who signaled.
        email_signaled_user (Optional[str]): Optional filter for the email of the signaled user.
        offset (int): The offset for pagination (skip the first N records).
        limit (int): The maximum number of records to return for pagination.

    Returns:
        SignaledUserListSchemaResponse: A response schema containing the filtered list of signaled users,
        including their IDs, the users involved, reasons, creation dates, and statuses. The response also
        includes the total count of signaled users matching the filter criteria.
    """
    signaled_users = signaled_user_service.get_signaled_users_by_filters(
        db,
        date,
        reason_id,
        user_id,
        signaled_user_id,
        status,
        email_user,
        email_signaled_user,
        offset,
        limit
    )
    total = signaled_user_service.get_signaled_users_by_filters_total_count(
        db,
        date,
        reason_id,
        user_id,
        signaled_user_id,
        status,
        email_user,
        email_signaled_user
    )

    all_signaled_users = []

    for signaled_user in signaled_users:

        user = user_service.get_user(db, signaled_user.user_signaled_id)

        signaled_by = user_service.get_user(db, signaled_user.user_id)

        reason = reason_service.get_reason_by_id(db, signaled_user.reason_id)

        all_signaled_users.append(
            SignaledUserSchemaResponse(
                id=signaled_user.id,
                user_signaled_id=user.id,
                user_signaled_email=user.email,
                reason=ReasonSchemaResponse(
                    id=reason.id,
                    reason=reason.reason
                ),
                signaled_by_id=signaled_by.id,
                signaled_by_email=signaled_by.email,
                created_at=signaled_user.created_at,
                status=signaled_user.status
            )
        )

    return SignaledUserListSchemaResponse(
        total=total,
        count=len(all_signaled_users),
        data=all_signaled_users
    )

def create_signaled_user_by_current(
    db: Session,
    signaled_user: SignaledUserCurrentUSerSchema,
    current_user: User
) -> bool:
    """
    Creates a new signaled user record in the database, initiated by the current user,
    indicating that the specified user has been reported for a certain reason.

    This function is used when a user reports another user for an issue or violation,
    and it records this action in the database for further moderation.

    Args:
        db (Session): The database session used to interact with the database.
        signaled_user (SignaledUserCurrentUSerSchema): A schema object containing the details
            of the signaled user, including the ID of the user being reported, the reason for the report,
            and other necessary data.
        current_user (User): The user who is initiating the report. This user is responsible for
            signaling the other user and will be recorded as the "reporting" user.

    Returns:
        bool: Returns `True` if the signaled user record was successfully created;
            otherwise, returns `False`.
    """
    return signaled_user_service.create_signaled_user(
        db=db,
        signaled_user_id=signaled_user.user_signaled_id,
        by_user_id=current_user.id,
        reason_id=signaled_user.reason_id
    )
