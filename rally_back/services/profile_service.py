from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import status

from models.profile_model import Profile
from enums.role import RoleEnum
from repositories import profile_repo
from errors import ProfileNotFound




def create_profile(db: Session, first_name: str, last_name: str, user_id: int, photo: str)->Profile:
    """used to create a profile"""
    new_profile = Profile(
                          user_id=user_id,
                          first_name=first_name,
                          last_name=last_name,
                          photo=photo,
                          nb_like=0,
                          created_at=datetime.now(),
                          updated_at=datetime.now()
                    )
    profile_repo.add_profile(db, new_profile)
    profile_repo.commit_profile(db)
    profile_repo.refresh_profile(db, new_profile)
    return new_profile

def get_profile(db: Session, profile_id: int)->Profile:
    """used to get a profile by its id"""
    profile = profile_repo.get_profile_by_id(db, profile_id)
    if not profile:
        raise ProfileNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    return profile

def update_profile(
    db: Session,
    profile_id: int,
    first_name: str,
    last_name: str,
    photo: str,
    nb_like: int
)->Profile:
    """used to update a profile"""
    profile = get_profile(db, profile_id)
    if not profile:
        raise ProfileNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    profile.first_name = first_name
    profile.last_name = last_name
    profile.photo = photo
    profile.nb_like = nb_like
    profile.updated_at = datetime.now()
    profile_repo.commit_profile(db)
    profile_repo.refresh_profile(db, profile)
    return profile

def update_profile_personal_infos(
    db: Session,
    profile_id: int,
    first_name: str,
    last_name: str,
    photo: str,
)->Profile:
    """used to update a profile"""
    profile = get_profile(db, profile_id)
    if not profile:
        raise ProfileNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    profile.first_name = first_name
    profile.last_name = last_name
    profile.photo = photo
    profile.updated_at = datetime.now()
    profile_repo.commit_profile(db)
    profile_repo.refresh_profile(db, profile)
    return profile

def delete_profile(db: Session, profile_id: int)->None:
    """used to delete a profile"""
    profile = get_profile(db, profile_id)
    if not profile:
        raise ProfileNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    profile_repo.delete_profile(db, profile)
    profile_repo.commit_profile(db)

def get_profiles_by_filters(
    db: Session,
    nb_like: Optional[int],
    is_planner: Optional[bool],
    role: Optional[RoleEnum],
    search: Optional[str],
    offset: int,
    limit: int
)->list[Profile]:
    """used to fetch profiles by given filters"""
    return profile_repo.get_all_profiles_by_filters(
        db,
        nb_like,
        is_planner,
        role,
        search,
        offset,
        limit
    )
    
    
def get_profiles_by_filters_total_count(
    db: Session,
    nb_like: Optional[int],
    is_planner: Optional[bool],
    role: Optional[RoleEnum],
    search: Optional[str],
)->int:
    """used to fetch profiles by given filters"""
    return profile_repo.get_all_profiles_by_filters_total_count(
        db,
        nb_like,
        is_planner,
        role,
        search,
    )
