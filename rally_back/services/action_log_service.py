from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session

from models.action_logs_model import ActionLog
from enums.action import ActionEnum
from enums.log_level import LogLevelEnum
from services import user_service
from repositories import action_log_repo
from errors import UserNotFoundError



def create_action_log(
    db: Session,
    user_id: int,
    log_type: LogLevelEnum,
    action_type: ActionEnum,
    description: str
) -> ActionLog:
    """
    Creates a new action log entry in the database.

    Parameters:
    - db (Session): The database session used for queries.
    - user_id (int): The ID of the user associated with the action.
    - log_type (LogLevelEnum): The level of the log (e.g., INFO, ERROR).
    - action_type (ActionEnum): The type of the action (e.g., CREATE, UPDATE).
    - description (str): A detailed description of the action performed.

    Raises:
    - UserNotFoundError: If the user with the specified user_id does not exist.

    Returns:
    - ActionLog: The created action log entry.
    """
    if not user_service.get_user(db, user_id):
        raise UserNotFoundError(status_code=404, detail="Utilisateur non trouvé.")

    new_action_log = ActionLog(
        user_id=user_id,
        log_type=log_type,
        action_type=action_type,
        description=description,
        date=datetime.now()
    )

    action_log_repo.add_action_log(db, new_action_log)
    action_log_repo.commit_action_log(db)
    action_log_repo.refresh_action_log(db, new_action_log)


def get_action_logs(
    db: Session,
    date: Optional[datetime],
    action_type: Optional[ActionEnum],
    user_id: Optional[int],
    log_type: Optional[LogLevelEnum],
    offset: int,
    limit: int
) -> list[ActionLog]:
    """
    Retrieves a list of action logs from the database with optional filters.

    Parameters:
    - db (Session): The database session used for queries.
    - date (Optional[datetime]): Filter logs by date (optional).
    - action_type (Optional[ActionEnum]): Filter logs by action type (optional).
    - user_id (Optional[int]): Filter logs by user ID (optional).
    - log_type (Optional[LogLevelEnum]): Filter logs by log type (optional).
    - offset (int): The offset (pagination) for the logs to retrieve.
    - limit (int): The maximum number of logs to retrieve.

    Returns:
    - list[ActionLog]: A list of action logs that match the provided filters.
    """
    return action_log_repo.get_action_logs_with_filters(
        db,
        date,
        action_type,
        user_id,
        log_type,
        offset,
        limit
    )
    
    
def get_action_logs_count(
    db: Session,
    date: Optional[datetime],
    action_type: Optional[ActionEnum],
    user_id: Optional[int],
    log_type: Optional[LogLevelEnum],
) -> int:
    """
    Retrieves a count of action logs from the database with optional filters.

    Parameters:
    - db (Session): The database session used for queries.
    - date (Optional[datetime]): Filter logs by date (optional).
    - action_type (Optional[ActionEnum]): Filter logs by action type (optional).
    - user_id (Optional[int]): Filter logs by user ID (optional).
    - log_type (Optional[LogLevelEnum]): Filter logs by log type (optional).
    """
    return action_log_repo.get_action_logs_with_filters_total_count(
        db,
        date,
        action_type,
        user_id,
        log_type
    )

