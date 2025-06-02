"""
This file contains the controller related to banned users
"""
from sqlalchemy.orm import Session
from fastapi import HTTPException
from services import (
    action_log_service,
    banned_user_service
)
from schemas.response_schemas.banned_user_schema_response import BannedUserSchemaResponse, BannedUserListSchemaResponse
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum
from models.user_model import User


def get_banned_users(db: Session, offset: int, limit: int) -> BannedUserListSchemaResponse:
    """
    Retrieves a list of banned users from the database, with pagination support.

    Args:
        db (Session): The database session used to interact with the banned user data.
        offset (int): The starting point for the pagination.
        limit (int): The maximum number of results to return.

    Returns:
        BannedUserListSchemaResponse: A response containing the count of banned users and the list of banned users.
    """
    banned_users = banned_user_service.get_banned_emails(db, offset, limit)

    all_banned_users = []

    for user in banned_users:
        all_banned_users.append(
            BannedUserSchemaResponse(
                id=user.id,
                banned_email=user.banned_email,
                banned_by_email=user.banned_by_email,
                banned_at=user.banned_at
            )
        )
    return BannedUserListSchemaResponse(
        count=len(all_banned_users),
        data=all_banned_users
    )


def get_banned_user_by_email(db: Session, email: str) -> BannedUserSchemaResponse:
    """
    Retrieves a banned user by their email address.

    Args:
        db (Session): The database session used to interact with the banned user data.
        email (str): The email address of the banned user.

    Returns:
        BannedUserSchemaResponse: A response containing the banned user's information.

    Raises:
        HTTPException: If no banned user is found with the provided email.
    """
    banned_user = banned_user_service.get_banned_user_by_email(db, email)

    if not banned_user:
        raise HTTPException(status_code=404, detail="La ressource n'a pas été trouvée")

    return BannedUserSchemaResponse(
        id=banned_user.id,
        banned_email=banned_user.banned_email,
        banned_by_email=banned_user.banned_by_email,
        banned_at=banned_user.banned_at
    )


def delete_banned_user(db: Session, email: str, current_user: User) -> bool:
    """
    Removes a banned user from the list of banned users and logs the action.

    Args:
        db (Session): The database session used to interact with the banned user data.
        email (str): The email address of the banned user to be removed.
        current_user (User): The current authenticated user who is performing the unbanning.

    Returns:
        bool: True if the user was successfully unbanned.

    Raises:
        HTTPException: If the user could not be found or deleted.
    """
    banned_user_service.delete_banned_user_by_email(db, email)
    action_log_service.create_action_log(
        db,
        current_user.id,
        LogLevelEnum.WARNING,
        ActionEnum.EMAIL_UNBANNED,
        f"User {current_user.email} removed email {email} from banned users"
    )
    return True
