"""
This file contains the controller related to action logs
"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from schemas.response_schemas.action_log_schema_response import ActionLogSchemaResponse, ActionLogListResponse
from services import action_log_service, role_service, user_service
from enums.action import ActionEnum
from enums.log_level import LogLevelEnum
from schemas.response_schemas.user_schema_response import UserResponse
from schemas.response_schemas.role_schema_response import RoleSchemaResponse

def get_action_logs(
    db: Session,
    date: Optional[datetime],
    action_type: Optional[ActionEnum],
    user_id: Optional[int],
    log_type: Optional[LogLevelEnum],
    offset: int,
    limit: int
) -> ActionLogListResponse:
    """
    Retrieve all action logs based on optional filtering parameters.

    Args:
        db (Session): SQLAlchemy database session.
        date (Optional[datetime]): Filter logs by a specific date.
        action_type (Optional[ActionEnum]): Filter by type of action.
        user_id (Optional[int]): Filter logs by user ID.
        log_type (Optional[LogLevelEnum]): Filter by log level.
        offset (int): Number of items to skip for pagination.
        limit (int): Maximum number of items to return.

    Returns:
        ActionLogListResponse: List of action logs matching the filters.
    """

    action_logs = action_log_service.get_action_logs(
        db,
        date,
        action_type,
        user_id,
        log_type,
        offset,
        limit
    )

    all_logs = []

    for log in action_logs:
        user = user_service.get_user(db, log.user_id)

        if user:

            role = role_service.get_role_by_id(db, user.role_id)

            role_schema = RoleSchemaResponse(
                id=role.id,
                role=role.role
            )

            user_schema = UserResponse(
                id=user.id,
                email=user.email,
                phone_number=user.phone_number,
                is_planner=user.is_planner,
                role=role_schema,
                account_id=user.account_id
            )
        else:
            user_schema = None

        all_logs.append(
            ActionLogSchemaResponse(
                id=log.id,
                logLevel=log.log_type,
                user=user_schema,
                actionType=log.action_type,
                description=log.description,
                date=log.date
            )
        )
    total = action_log_service.get_action_logs_count(
        db,
        date,
        action_type,
        user_id,
        log_type
    )

    return ActionLogListResponse(count=len(all_logs), data=all_logs, total=total)
