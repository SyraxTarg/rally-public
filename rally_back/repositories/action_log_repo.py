"""This file contains the action log repository"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from models.action_logs_model import ActionLog
from enums.action import ActionEnum
from enums.log_level import LogLevelEnum


def add_action_log(db: Session, action_log: ActionLog):
    """
    Add new action log in database

    Args:
        db (Session): The database session used to interact with the database.
        action_log (ActionLog): The action log object to add.
    """
    db.add(action_log)

def commit_action_log(db: Session):
    """
    Commit the changes in the database

    Args:
        db (Session): The database session used to interact with the database.
    """
    db.commit()

def refresh_action_log(db: Session, action_log: ActionLog):
    """
    Refreshing the changes from the db

    Args:
        db (Session): The database session used to interact with the database.
        action_log (ActionLog): The action log object to refresh in the database.
    """
    db.refresh(action_log)

def get_action_logs_with_filters(
    db: Session,
    date: Optional[datetime],
    action_type: Optional[ActionEnum],
    user_id: Optional[int],
    log_type: Optional[LogLevelEnum],
    offset: int,
    limit: int
) -> list[ActionLog]:
    """
    Returns all the action logs from the database according to filters.

    Args:
        db (Session): The database session used to interact with the database.
        date (Optional[datetime]): date filter
        action_type (Optional[ActionEnum]): action type filter
        user_id (Optional[int]): user id filter
        log_type (Optional[LogLevelEnum]): log type filter
        offset (int): offset for pagination
        limit (int): limit for pagination

    Returns:
        A list of action logs from the database.
    """
    query = db.query(ActionLog)

    if date is not None:
        query = query.filter(func.date(ActionLog.date) == date.date())

    if action_type is not None:
        query = query.filter(ActionLog.action_type == action_type)

    if user_id is not None:
        query = query.filter(ActionLog.user_id == user_id)

    if log_type is not None:
        query = query.filter(ActionLog.log_type == log_type)

    return query.order_by(ActionLog.date.desc()).offset(offset).limit(limit).all()

def get_action_logs_with_filters_total_count(
    db: Session,
    date: Optional[datetime],
    action_type: Optional[ActionEnum],
    user_id: Optional[int],
    log_type: Optional[LogLevelEnum],
) -> int:
    """
    Returns the count of the action logs from the database according to filters.

    Args:
        db (Session): The database session used to interact with the database.
        date (Optional[datetime]): date filter
        action_type (Optional[ActionEnum]): action type filter
        user_id (Optional[int]): user id filter
        log_type (Optional[LogLevelEnum]): log type filter

    Returns:
        A list of action logs from the database.
    """
    query = db.query(ActionLog)

    if date is not None:
        query = query.filter(func.date(ActionLog.date) == date.date())

    if action_type is not None:
        query = query.filter(ActionLog.action_type == action_type)

    if user_id is not None:
        query = query.filter(ActionLog.user_id == user_id)

    if log_type is not None:
        query = query.filter(ActionLog.log_type == log_type)

    return query.order_by(ActionLog.date.desc()).count()

