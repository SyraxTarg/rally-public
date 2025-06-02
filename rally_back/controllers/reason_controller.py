"""
This file contains the controller related to reasons
"""
from datetime import datetime
from sqlalchemy.orm import Session
from schemas.request_schemas.reason_schema import ReasonSchema
from schemas.response_schemas.reason_schema_response import ReasonSchemaResponse, ReasonListSchemaResponse
from services import action_log_service, reason_service
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum
from models.user_model import User


def create_reason(db: Session, reason: ReasonSchema, current_user: User) -> ReasonSchemaResponse:
    """
    Creates a new reason in the database.

    Args:
        db (Session): The database session used to interact with the database.
        reason (ReasonSchema): The reason data to be added.
        current_user (User): The user performing the action.

    Returns:
        ReasonSchemaResponse: The response containing the newly created reason's details.

    Logs the action of creating the reason for auditing purposes.
    """
    reason = reason_service.create_reason(db, reason.reason)

    action_log_service.create_action_log(
        db,
        current_user.id,
        LogLevelEnum.INFO,
        ActionEnum.REASON_CREATED,
        f"User {current_user.id} added reason {reason.id} at {datetime.now()} by {current_user.email}"
    )

    return ReasonSchemaResponse(
        id=reason.id,
        reason=reason.reason
    )

def get_reasons(db: Session) -> ReasonListSchemaResponse:
    """
    Retrieves a list of reasons from the database.

    Args:
        db (Session): The database session used to interact with the database.
        offset (int): The starting point for pagination.
        limit (int): The maximum number of results to return.

    Returns:
        ReasonListSchemaResponse: The response containing the list of reasons.

    This function fetches the reasons with the given pagination parameters and returns them.
    """
    reasons = reason_service.get_reasons(db)
    all_reasons = []
    for reason in reasons:
        all_reasons.append(
            ReasonSchemaResponse(
                id=reason.id,
                reason=reason.reason
            )
        )
    return ReasonListSchemaResponse(
        count=len(all_reasons),
        data=all_reasons
    )

def get_reason_by_id(db: Session, reason_id: int) -> ReasonSchemaResponse:
    """
    Retrieves a specific reason by its ID from the database.

    Args:
        db (Session): The database session used to interact with the database.
        reason_id (int): The ID of the reason to retrieve.

    Returns:
        ReasonSchemaResponse: The reason details for the specified ID.

    This function fetches the reason by the given ID and returns it in a response schema.
    """
    reason = reason_service.get_reason_by_id(db, reason_id)
    return ReasonSchemaResponse(
        id=reason.id,
        reason=reason.reason
    )

def delete_reason(db: Session, reason_id: int, current_user: User) -> dict[str, str]:
    """
    Deletes a reason from the database based on the provided ID.

    Args:
        db (Session): The database session used to interact with the database.
        reason_id (int): The ID of the reason to be deleted.
        current_user (User): The user performing the deletion action.

    Returns:
        dict[str, str]: A dictionary with a success message indicating that the reason was deleted.

    This function deletes the reason with the specified ID and logs the action in the system's action log.
    """
    reason_service.delete_reason(db, reason_id)

    action_log_service.create_action_log(
        db,
        current_user.id,
        LogLevelEnum.INFO,
        ActionEnum.REASON_DELETED,
        f"User {current_user.id} releted reason {reason_id} at {datetime.now()} by {current_user.email}"
    )

    return {"msg": "supprime"}
