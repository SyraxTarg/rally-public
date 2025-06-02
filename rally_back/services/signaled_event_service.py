from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status

from models.signaled_events_model import SignaledEvent
from repositories import signaled_event_repo
from errors import SignaledEventNotFound




def create_signaled_event(
    db: Session,
    event_id: int,
    user_id: int,
    reason_id: int
)->SignaledEvent:
    """used to create a new signaled event"""
    signaled_event = SignaledEvent(
        event_id=event_id,
        reason_id=reason_id,
        created_at=datetime.now(),
        user_id=user_id,
        status="pending"
    )
    signaled_event_repo.add_signaled_event(db, signaled_event)
    signaled_event_repo.commit_signaled_events(db)
    signaled_event_repo.refresh_signaled_event(db, signaled_event)
    return True

def get_signaled_events(db: Session)->list[SignaledEvent]:
    """used to get all signaled events"""
    return signaled_event_repo.get_signaled_events(db)

def get_signaled_event_by_event_id(db: Session, event_id: int)->list[SignaledEvent]:
    """used to get signaled events by event id"""
    return signaled_event_repo.get_signaled_events_by_event_id(db, event_id)

def get_signaled_event_by_id(db: Session, signaled_event_id: int)->SignaledEvent:
    """used to get a signaled event by its id"""
    signaled_event = signaled_event_repo.get_signaled_event_by_id(db, signaled_event_id)
    if not signaled_event:
        raise SignaledEventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Signaled event not found"
        )
    return signaled_event

def update_status_signaled_event(db: Session, signaled_event_id: int, status: str)->SignaledEvent:
    """used to update the status of a signaled event"""
    signaled_event = get_signaled_event_by_id(db, signaled_event_id)
    if not signaled_event:
        raise SignaledEventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Signaled event not found"
        )
    signaled_event.status = status
    signaled_event_repo.commit_signaled_events(db)
    signaled_event_repo.refresh_signaled_event(db, signaled_event)
    return signaled_event

def get_signaled_events_by_filters(
    db: Session,
    date: Optional[datetime],
    reason_id: Optional[int],
    user_id: Optional[int],
    event_id: Optional[int],
    status: Optional[str],
    email_user: Optional[str],
    email_event_user: Optional[str],
    offset: int,
    limit: int
)->list[SignaledEvent]:
    """used to get signaled events according to given filters"""
    return signaled_event_repo.get_signaled_events_filters(
        db,
        date,
        reason_id,
        user_id,
        event_id,
        status,
        email_user,
        email_event_user,
        offset,
        limit
    )
