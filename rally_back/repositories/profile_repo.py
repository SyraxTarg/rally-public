"""This file contains the profile repository"""
from typing import Optional
from sqlalchemy import or_
from sqlalchemy.orm import Session
from models.profile_model import Profile
from models.user_model import  User
from enums.role import RoleEnum
from models.role_model import Role

def add_profile(db: Session, profile: Profile)->None:
    """
    This function is used to add a new profile in db.
    """
    db.add(profile)

def commit_profile(db: Session)->None:
    """
    This function is used to commit changes in db.
    """
    db.commit()

def refresh_profile(db: Session, profile: Profile)->None:
    """
    This function is used to refresh a profile.
    """
    db.refresh(profile)

def get_profile_by_id(db: Session, profile_id: int)->Profile:
    """
    This function is used to fetch a profile by its id.
    """
    return db.query(Profile).filter(Profile.id == profile_id).first()

def delete_profile(db: Session, profile: Profile)->None:
    """Used to delete a profile"""
    db.delete(profile)

def get_all_profiles_by_filters(
    db: Session,
    nb_like: Optional[int],
    is_planner: Optional[bool],
    role: Optional[RoleEnum],
    search: Optional[str],
    offset: int,
    limit: int
)->list[Profile]:
    """Used to get all profiles according to given filters."""
    query = db.query(Profile).join(User).join(Role)

    if nb_like is not None:
        query = query.filter(Profile.nb_like <= nb_like)

    if is_planner is not None:
        query = query.filter(User.is_planner == is_planner)

    if role is not None:
        query = query.filter(Role.role == role.value)

    if search is not None:
        query = query.filter(
            or_(
                Profile.first_name.ilike(f"%{search}%"),
                Profile.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    return query.offset(offset).limit(limit).all()


def get_all_profiles_by_filters_total_count(
    db: Session,
    nb_like: Optional[int],
    is_planner: Optional[bool],
    role: Optional[RoleEnum],
    search: Optional[str],
)->int:
    """Used to get all profiles according to given filters."""
    query = db.query(Profile).join(User).join(Role)

    if nb_like is not None:
        query = query.filter(Profile.nb_like <= nb_like)

    if is_planner is not None:
        query = query.filter(User.is_planner == is_planner)

    if role is not None:
        query = query.filter(Role.role == role.value)

    if search is not None:
        query = query.filter(
            or_(
                Profile.first_name.ilike(f"%{search}%"),
                Profile.last_name.ilike(f"%{search}%"),
                User.email.ilike(f"%{search}%")
            )
        )

    return query.count()
