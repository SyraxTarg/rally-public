from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import status

from models.signaled_users_model import SignaledUser
from services import role_service, user_service
from enums.role import RoleEnum
from repositories import signaled_user_repo
from errors import (
    SignaledUserNotFound,
    BadRoleError,
    UserNotFoundError,
    RoleNotFound
)


def create_signaled_user(
    db: Session,
    signaled_user_id: int,
    by_user_id: int,
    reason_id: int
)->SignaledUser:
    """used to create a new signaled user"""
    user_signaled = user_service.get_user(db, signaled_user_id)
    if not user_signaled:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    role = role_service.get_role_by_id(db, user_signaled.role_id)
    if not role:
        raise RoleNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    if role.role in (RoleEnum.ROLE_ADMIN, RoleEnum.ROLE_SUPER_ADMIN):
        raise BadRoleError(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez pas signaler cet utilisateur"
        )

    signaled_user = SignaledUser(
        user_signaled_id=signaled_user_id,
        reason_id=reason_id,
        created_at=datetime.now(),
        user_id=by_user_id,
        status="pending"
    )
    signaled_user_repo.add_signaled_user(db, signaled_user)
    signaled_user_repo.commit_signaled_user(db)
    signaled_user_repo.refresh_signaled_user(db, signaled_user)
    return True

def get_signaled_user_by_id(db: Session, user_signaled_id: int)->list[SignaledUser]:
    """used to get a signaled user by the id of the user signaled"""
    return signaled_user_repo.get_signaled_user_by_user_signaled_id(db, user_signaled_id)



def get_signaled_user(db: Session, signaled_user_id: int)->Optional[SignaledUser]:
    """used to get a signaled user by its id"""
    signaled_user = signaled_user_repo.get_signaled_user_by_id(db, signaled_user_id)
    if not signaled_user:
        raise SignaledUserNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Signaled user not found"
        )
    return signaled_user

def get_signaled_user_by_user_by_id(db: Session, user_id: int)->list[SignaledUser]:
    """used to get a signaled user by the id of the user that signaled someone"""
    return signaled_user_repo.get_signaled_user_by_user_id(db, user_id)

def update_status_signaled_user(db: Session, signaled_user_id: int, status_: str)->SignaledUser:
    """used to update the status of a signaled user"""
    signaled_user = get_signaled_user_by_id(db, signaled_user_id)
    if not signaled_user:
        raise SignaledUserNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Signaled user not found"
        )
    signaled_user.status = status_
    signaled_user_repo.commit_signaled_user(db)
    signaled_user_repo.refresh_signaled_user(db, signaled_user)
    return signaled_user

def get_signaled_users_by_filters(
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
)->list[SignaledUser]:
    """used to get signaled users according to given filters"""
    return signaled_user_repo.get_signaled_users_filters(
        db,
        date,
        reason_id,
        user_id,
        signaled_user_id,
        status,
        email_user,
        email_signaled_user,
        offset,
        limit
    )


def get_signaled_users_by_filters_total_count(
    db: Session,
    date: Optional[datetime],
    reason_id: Optional[int],
    user_id: Optional[int],
    signaled_user_id: Optional[int],
    status: Optional[str],
    email_user: Optional[str],
    email_signaled_user: Optional[str],
)->int:
    """used to get signaled users according to given filters"""
    return signaled_user_repo.get_signaled_users_filters_total_count(
        db,
        date,
        reason_id,
        user_id,
        signaled_user_id,
        status,
        email_user,
        email_signaled_user,
    )

