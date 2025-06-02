from typing import Optional
import re
from sqlalchemy.orm import Session
from fastapi import status

from services import profile_service, role_service
from models.role_model import Role
from models.user_model import User
from core.security import hash_password
from enums.role import RoleEnum
from errors import UserNotFoundError, InvalidEmailFormat, RoleNotFound

from repositories import user_repo



def is_valid_email(email: str) -> bool:
    """used to verify if a given email is valid or not"""
    regex = r"[^@]+@[^@]+\.[^@]+"
    return re.match(regex, email) is not None

def get_user(db: Session, user_id: int)->User:
    """used to get a user by its id"""
    return user_repo.get_user_by_id(db, user_id)

def get_user_by_email(db: Session, email: str)->User:
    """used to get a user by its email"""
    return user_repo.get_user_by_email(db, email)

def create_user(
    db: Session,
    email: str,
    password: str,
    phone_number: str,
    first_name: str,
    last_name: str,
    photo: str
) -> User:
    """used to create a new user"""
    if not is_valid_email(email):
        raise InvalidEmailFormat(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    hashed_password = hash_password(password)
    role_user = role_service.get_role_user(db)
    if not role_user:
        role_user = role_service.create_role_user(db)

    if photo:
        photo_name = photo
    else:
        photo_name = "default.jpg"

    new_user = User(
        email=email,
        password=hashed_password,
        phone_number=phone_number,
        is_planner=False,
        role_id=role_user.id,
        is_verified= False,
    )
    user_repo.add_user(db, new_user)
    user_repo.commit_user(db)
    user_repo.refresh_user(db, new_user)
    profile_service.create_profile(db, first_name, last_name, new_user.id, photo_name)
    return new_user

def create_admin(
    db: Session,
    email: str,
    password: str,
    phone_number: str,
    first_name: str,
    last_name: str,
    photo: str
)->User:
    """used to create a new admin"""
    if not is_valid_email(email):
        raise InvalidEmailFormat(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    hashed_password = hash_password(password)
    role_admin = role_service.get_role_admin(db)
    if not role_admin:
        role_admin = role_service.create_role_admin(db)

    if photo:
        photo_name=photo
    else:
        photo_name = "default.jpg"

    new_user = User(
        email=email,
        password=hashed_password,
        phone_number=phone_number,
        is_planner=False,
        role_id=role_admin.id,
        is_verified= False,
    )
    user_repo.add_user(db, new_user)
    user_repo.commit_user(db)
    user_repo.refresh_user(db, new_user)
    profile_service.create_profile(db, first_name, last_name, new_user.id, photo_name)
    return new_user

def create_super_admin(
    db: Session,
    email: str,
    password: str,
    phone_number: str,
    first_name: str,
    last_name: str,
    photo: str
)->User:
    """used to create a new super admin"""
    if not is_valid_email(email):
        raise InvalidEmailFormat(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )

    hashed_password = hash_password(password)
    role_super_admin = role_service.get_role_super_admin(db)
    if not role_super_admin:
        role_super_admin = role_service.create_role_super_admin(db)

    if photo:
        photo_name=photo
    else:
        photo_name = "default.jpg"

    new_user = User(
        email=email,
        password=hashed_password,
        phone_number=phone_number,
        is_planner=False,
        role_id=role_super_admin.id,
        is_verified= False,
    )
    user_repo.add_user(db, new_user)
    user_repo.commit_user(db)
    user_repo.refresh_user(db, new_user)
    profile_service.create_profile(db, first_name, last_name, new_user.id, photo_name)
    return new_user

def update_user(
    db: Session,
    user_id: int,
    email: str,
    phone_number: str,
    is_planner: bool
)->User:
    """used to update a user"""
    user = get_user(db, user_id)
    if not user:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.email = email
    user.phone_number = phone_number
    user.is_planner = is_planner
    user_repo.commit_user(db)
    user_repo.refresh_user(db, user)
    return user

def update_user_phone_number(
    db: Session,
    user_id: int,
    phone_number: str,
)->User:
    """used to update a user"""
    user = get_user(db, user_id)
    if not user:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.phone_number = phone_number
    user_repo.commit_user(db)
    user_repo.refresh_user(db, user)
    return user

def search_users(db: Session, search: Optional[str], offset: int, limit: int)->list[User]:
    """used to search users according to search string"""
    return user_repo.search_users(db, search, offset, limit)

def toggle_is_planner(db: Session, user_id: int)->User:
    """used to toggle the is_planner attribute (boolean) from a user"""
    user = get_user(db, user_id)
    if not user:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    if user.is_planner is True:
        user.is_planner = False
    else:
        user.is_planner = True
    user_repo.commit_user(db)
    user_repo.refresh_user(db, user)
    return user

def grant_role(db: Session, role: Role, user: User)->User:
    """used to grant a role to a user"""
    user.role_id = role.id
    user_repo.commit_user(db)
    user_repo.refresh_user(db, user)
    return user

def is_admin(db: Session, user_id: int) -> bool:
    """used to verify if user has role admin"""
    user = get_user(db, user_id)

    if not user:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    role = role_service.get_role_by_id(db, user.role_id)
    if not role:
        raise RoleNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Role not found"
        )

    return role.role == RoleEnum.ROLE_ADMIN or role.role == RoleEnum.ROLE_SUPER_ADMIN

def update_stripe_account(db: Session, user_id: int, account_id: str)->User:
    """used to update the stripe account id attribute from user"""
    user = get_user(db, user_id)
    if not user:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    user.account_id = account_id
    user_repo.commit_user(db)
    user_repo.refresh_user(db, user)
    return user
