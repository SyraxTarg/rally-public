from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status

from models.signaled_comments_model import SignaledComment
from repositories import signaled_comment_repo
from errors import SignaledCommentNotFound




def create_signaled_comment(
    db: Session,
    comment_id: int,
    user_id: int,
    reason_id: int
)->SignaledComment:
    """used to create a new signaled comment"""
    signaled_comment = SignaledComment(
        comment_id=comment_id,
        reason_id=reason_id,
        created_at=datetime.now(),
        user_id=user_id,
        status="pending"
    )
    signaled_comment_repo.add_signaled_comment(db, signaled_comment)
    signaled_comment_repo.commit_signaled_comment(db)
    signaled_comment_repo.refresh_signaled_comment(db, signaled_comment)
    return True

def get_signaled_comments(db: Session)->list[SignaledComment]:
    """used to get signaled comments"""
    return signaled_comment_repo.get_signaled_comments(db)

def get_signaled_comment_by_comment_id(db: Session, comment_id: int)->list[SignaledComment]:
    """used to get signaled comments by their comment id"""
    return signaled_comment_repo.get_signaled_comments_by_comment_id(db, comment_id)

def get_signaled_comment_by_id(db: Session, signaled_comment_id: int)->SignaledComment:
    """used to get signaled comment by its id"""
    signaled_comment = signaled_comment_repo.get_signaled_comment_by_id(db, signaled_comment_id)
    if not signaled_comment:
        raise SignaledCommentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ressource not found"
        )
    return signaled_comment

def get_signaled_comment_by_user_by_id(db: Session, user_id: int)->SignaledComment:
    """used to get signaled comment by its user id"""
    signaled_comment = signaled_comment_repo.get_signaled_comment_by_user_id(db, user_id)
    if not signaled_comment:
        raise SignaledCommentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ressource not found"
        )
    return signaled_comment

def get_signaled_comment_by_reason_id(db: Session, reason_id: int)->list[SignaledComment]:
    """used to get signaled comments by the reason id"""
    return signaled_comment_repo.get_signaled_comment_by_reason_id(db, reason_id)

def get_signaled_comment_by_status(db: Session, status: str)->list[SignaledComment]:
    """used to get signaled comments by status"""
    return signaled_comment_repo.get_signaled_comment_by_status(db, status)

def update_status_signaled_comment(db: Session, signaled_comment_id: int, status_: str)->SignaledComment:
    """used to update the status of a signaled comment"""
    signaled_comment = get_signaled_comment_by_id(db, signaled_comment_id)
    if not signaled_comment:
        raise SignaledCommentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ressource not found"
        )
    signaled_comment.status = status_
    signaled_comment_repo.commit_signaled_comment(db)
    signaled_comment_repo.refresh_signaled_comment(db, signaled_comment)
    return signaled_comment

def get_signaled_comments_by_filters(
    db: Session,
    date: Optional[datetime],
    reason_id: Optional[int],
    user_id: Optional[int],
    comment_id: Optional[int],
    status: Optional[str],
    email_user: Optional[str],
    email_comment_user: Optional[str],
    offset: int,
    limit: int
)->list[SignaledComment]:
    """used to get signaled comments according to given filters"""
    return signaled_comment_repo.get_signaled_comments_filters(
        db,
        date,
        reason_id,
        user_id,
        comment_id,
        status,
        email_user,
        email_comment_user,
        offset,
        limit
    )
