"""This file contains the signaled event repository"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session, aliased
from models.signaled_events_model import SignaledEvent
from models.user_model import User
from models.event_model import Event
from models.profile_model import Profile

def add_signaled_event(db: Session, signaled_event: SignaledEvent) -> None:
    """Add a new signaled event to the database."""
    db.add(signaled_event)

def commit_signaled_events(db: Session) -> None:
    """Commit the current transaction for signaled events."""
    db.commit()

def refresh_signaled_event(db: Session, signaled_event: SignaledEvent) -> None:
    """Refresh the state of a signaled event from the database."""
    db.refresh(signaled_event)

def delete_signaled_event(db: Session, signaled_event: SignaledEvent) -> None:
    """Delete a signaled event from the database."""
    db.delete(signaled_event)

def get_signaled_events(db: Session) -> list[SignaledEvent]:
    """Retrieve all signaled events from the database."""
    return db.query(SignaledEvent).all()

def get_signaled_events_by_event_id(db: Session, event_id: int) -> list[SignaledEvent]:
    """Retrieve signaled events associated with a specific event ID."""
    return db.query(SignaledEvent).filter(SignaledEvent.event_id == event_id).all()

def get_signaled_event_by_id(db: Session, signaled_event_id: int) -> SignaledEvent:
    """Retrieve a single signaled event by its ID."""
    return db.query(SignaledEvent).filter(SignaledEvent.id == signaled_event_id).first()

def get_signaled_events_filters(
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
) -> list[SignaledEvent]:
    """Retrieve signaled events based on optional filters like date, reason, user, event, status or emails."""
    query = db.query(SignaledEvent)

    if date is not None:
        query = query.filter(SignaledEvent.created_at <= date)

    if reason_id is not None:
        query = query.filter(SignaledEvent.reason_id == reason_id)

    if user_id is not None:
        query = query.filter(SignaledEvent.user_id == user_id)

    if event_id is not None:
        query = query.filter(SignaledEvent.event_id == event_id)

    if status is not None:
        query = query.filter(SignaledEvent.status == status)

    # alias pour pas de conflits
    profile_alias = aliased(Profile)
    event_owner_alias = aliased(User)
    event_alias = aliased(Event)
    user_alias = aliased(User)

    if email_user is not None:
        query = query.join(user_alias, SignaledEvent.user).filter(user_alias.email == email_user)

    if email_event_user is not None:
        query = (
            query
            .join(event_alias, SignaledEvent.event)
            .join(profile_alias, event_alias.profile)
            .join(event_owner_alias, profile_alias.user)
            .filter(event_owner_alias.email == email_event_user)
        )

    return query.order_by(SignaledEvent.created_at.desc()).offset(offset).limit(limit).all()
