"""This file contains the signaled comment repository"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session, aliased
from models.signaled_comments_model import SignaledComment
from models.user_model import User
from models.profile_model import Profile
from models.comment_model import Comment

def add_signaled_comment(db: Session, signaled_comment: SignaledComment) -> None:
    """Add a new signaled comment to the database."""
    db.add(signaled_comment)

def commit_signaled_comment(db: Session) -> None:
    """Commit the current transaction for signaled comments."""
    db.commit()

def refresh_signaled_comment(db: Session, signaled_comment: SignaledComment) -> None:
    """Refresh the state of a signaled comment from the database."""
    db.refresh(signaled_comment)

def delete_signaled_comment(db: Session, signaled_comment: SignaledComment) -> None:
    """Delete a signaled comment from the database."""
    db.delete(signaled_comment)

def get_signaled_comments(db: Session) -> list[SignaledComment]:
    """Retrieve all signaled comments."""
    return db.query(SignaledComment).all()

def get_signaled_comments_by_comment_id(db: Session, comment_id: int) -> list[SignaledComment]:
    """Retrieve signaled comments by comment ID."""
    return db.query(SignaledComment).filter(SignaledComment.comment_id == comment_id).all()

def get_signaled_comment_by_id(db: Session, signaled_comment_id: int) -> SignaledComment:
    """Retrieve a signaled comment by its ID."""
    return db.query(SignaledComment).filter(SignaledComment.id == signaled_comment_id).first()

def get_signaled_comment_by_user_id(db: Session, user_id: int) -> SignaledComment:
    """Retrieve a signaled comment made by a specific user ID."""
    return db.query(SignaledComment).filter(SignaledComment.user_id == user_id).first()

def get_signaled_comment_by_reason_id(db: Session, reason_id: int) -> list[SignaledComment]:
    """Retrieve signaled comments by reason ID."""
    return db.query(SignaledComment).filter(SignaledComment.reason_id == reason_id).all()

def get_signaled_comment_by_status(db: Session, status: str) -> list[SignaledComment]:
    """Retrieve signaled comments by their status."""
    return db.query(SignaledComment).filter(SignaledComment.status == status).all()

def get_signaled_comments_filters(
    db: Session,
    date: Optional[datetime] = None,
    reason_id: Optional[int] = None,
    user_id: Optional[int] = None,
    comment_id: Optional[int] = None,
    status: Optional[str] = None,
    email_user: Optional[str] = None,
    email_comment_user: Optional[str] = None,
    offset: Optional[int] = 5,
    limit: Optional[int] = 5
) -> list[SignaledComment]:
    """Retrieve signaled comments using optional filters: date, reason, user, comment, status, or emails."""
    query = db.query(SignaledComment)

    if date is not None:
        query = query.filter(SignaledComment.created_at <= date)

    if reason_id is not None:
        query = query.filter(SignaledComment.reason_id == reason_id)

    if user_id is not None:
        query = query.filter(SignaledComment.user_id == user_id)

    if comment_id is not None:
        query = query.filter(SignaledComment.comment_id == comment_id)

    if status is not None:
        query = query.filter(SignaledComment.status == status)

    # 🔁 ALIAS pour éviter conflit
    user_alias = aliased(User)
    profile_alias = aliased(Profile)
    comment_owner_alias = aliased(User)
    comment_alias = aliased(Comment)

    if email_user is not None:
        query = query.join(user_alias, SignaledComment.user).filter(user_alias.email == email_user)

    if email_comment_user is not None:
        query = (
            query
            .join(comment_alias, SignaledComment.comment_signaled)
            .join(profile_alias, comment_alias.profile)
            .join(comment_owner_alias, profile_alias.user)
            .filter(comment_owner_alias.email == email_comment_user)
        )

    return query.order_by(SignaledComment.created_at.desc()).offset(offset).limit(limit).all()
