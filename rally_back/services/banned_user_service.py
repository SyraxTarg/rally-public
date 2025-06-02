from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status

from models.banned_user_model import BannedUser
from repositories import banned_user_repo
from errors import BannedUserNotFoundError



def create_banned_user(db: Session, banned_email: str, banned_by_email: str) -> BannedUser:
    """used to create a banned user"""
    banned_user = get_banned_user_by_email(db, banned_email)
    if banned_user is not None:
        return banned_user

    new_banned_user = BannedUser(
        banned_email = banned_email,
        banned_by_email = banned_by_email,
        banned_at = datetime.now()
    )

    banned_user_repo.add_new_banned_user(db, new_banned_user)
    banned_user_repo.commit_banned_user(db)
    banned_user_repo.refresh_banned_user(db, new_banned_user)
    return new_banned_user

def get_banned_user_by_email(db: Session, email: str) -> Optional[BannedUser]:
    """used to fetch banned user by email"""
    return banned_user_repo.get_banned_user_by_email(db, email)

def delete_banned_user_by_email(db: Session, email: str) -> bool:
    """used to delete banned user by email"""
    banned_user = get_banned_user_by_email(db, email)
    if not banned_user:
        raise BannedUserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Banned user not found"
        )

    banned_user_repo.delete_banned_user(db, banned_user)
    banned_user_repo.commit_banned_user(db)
    return True

def get_banned_emails(db: Session, offset: int, limit: int) -> list[BannedUser]:
    """used to get all banned emails"""
    return banned_user_repo.get_all_banned_emails(db, offset, limit)
