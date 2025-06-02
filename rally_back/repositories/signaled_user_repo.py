"""This file contains the signaled user repository"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session, aliased
from models.signaled_users_model import SignaledUser
from models.user_model import User

def add_signaled_user(db: Session, signaled_user: SignaledUser) -> None:
    """Add a new signaled user to the database."""
    db.add(signaled_user)

def commit_signaled_user(db: Session) -> None:
    """Commit the current transaction for signaled users."""
    db.commit()

def refresh_signaled_user(db: Session, signaled_user: SignaledUser) -> None:
    """Refresh the state of a signaled user from the database."""
    db.refresh(signaled_user)

def delete_signaled_user(db: Session, signaled_user: SignaledUser) -> None:
    """Delete a signaled user from the database."""
    db.delete(signaled_user)

def get_signaled_user_by_user_signaled_id(db: Session, user_signaled_id: int) -> list[SignaledUser]:
    """Retrieve signaled users by the ID of the user who was reported."""
    return db.query(SignaledUser).filter(SignaledUser.user_signaled_id == user_signaled_id).all()

def get_signaled_user_by_id(db: Session, signaled_user_id: int) -> Optional[SignaledUser]:
    """Retrieve a specific signaled user by its ID."""
    return db.query(SignaledUser).filter(SignaledUser.id == signaled_user_id).first()

def get_signaled_user_by_user_id(db: Session, user_id: int) -> list[SignaledUser]:
    """Retrieve signaled users by the ID of the user who reported."""
    return db.query(SignaledUser).filter(SignaledUser.user_id == user_id).all()

def get_signaled_users_filters(
    db: Session,
    date: Optional[datetime],
    reason_id: Optional[int],
    user_id: Optional[int],
    signaled_user_id: Optional[int],
    status: Optional[str],
    email_user: Optional[str],
    email_signaled_user: Optional[str],
    offset: int,
    limit: int
) -> list[SignaledUser]:
    """Retrieve signaled users using optional filters like date, reason, user, reported user, status or emails."""
    query = db.query(SignaledUser)

    if date is not None:
        query = query.filter(SignaledUser.created_at <= date)

    if reason_id is not None:
        query = query.filter(SignaledUser.reason_id == reason_id)

    if user_id is not None:
        query = query.filter(SignaledUser.user_id == user_id)

    if signaled_user_id is not None:
        query = query.filter(SignaledUser.user_signaled_id == signaled_user_id)

    if status is not None:
        query = query.filter(SignaledUser.status == status)

    # ALIAS pour éviter conflit
    user_alias = aliased(User)
    signaled_user_alias = aliased(User)

    if email_user is not None:
        query = query.join(user_alias, SignaledUser.user).filter(user_alias.email == email_user)

    if email_signaled_user is not None:
        query = query.join(signaled_user_alias, SignaledUser.user_signaled).filter(signaled_user_alias.email == email_signaled_user)

    return query.order_by(SignaledUser.created_at.desc()).offset(offset).limit(limit).all()


def get_signaled_users_filters_total_count(
    db: Session,
    date: Optional[datetime],
    reason_id: Optional[int],
    user_id: Optional[int],
    signaled_user_id: Optional[int],
    status: Optional[str],
    email_user: Optional[str],
    email_signaled_user: Optional[str],
) -> int:
    """Retrieve signaled users using optional filters like date, reason, user, reported user, status or emails."""
    query = db.query(SignaledUser)

    if date is not None:
        query = query.filter(SignaledUser.created_at <= date)

    if reason_id is not None:
        query = query.filter(SignaledUser.reason_id == reason_id)

    if user_id is not None:
        query = query.filter(SignaledUser.user_id == user_id)

    if signaled_user_id is not None:
        query = query.filter(SignaledUser.user_signaled_id == signaled_user_id)

    if status is not None:
        query = query.filter(SignaledUser.status == status)

    # ALIAS pour éviter conflit
    user_alias = aliased(User)
    signaled_user_alias = aliased(User)

    if email_user is not None:
        query = query.join(user_alias, SignaledUser.user).filter(user_alias.email == email_user)

    if email_signaled_user is not None:
        query = query.join(signaled_user_alias, SignaledUser.user_signaled).filter(signaled_user_alias.email == email_signaled_user)

    return query.order_by(SignaledUser.created_at.desc()).count()

