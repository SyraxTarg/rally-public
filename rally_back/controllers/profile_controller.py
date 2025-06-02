"""
This file contains the controller related to profiles
"""
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException

from schemas.response_schemas.user_schema_response import UserResponse
from schemas.response_schemas.role_schema_response import RoleSchemaResponse
from schemas.response_schemas.profile_schema_response import (
    ProfileSchemaResponse,
    ProfileListSchemaResponse,
    ProfileRestrictedSchemaResponse,
    ProfileRestrictedListSchemaResponse
)
from schemas.request_schemas.profile_schema import ProfileSchema, ModifyProfileSchema
from services import (
    action_log_service,
    moderation_service,
    profile_service,
    role_service,
    user_service
)
from enums.role import RoleEnum
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum


def get_profile(db: Session, profile_id: int) -> ProfileSchemaResponse:
    """
    Retrieves a profile by its ID, along with the associated user and role details.

    This function fetches a user's profile by ID, then retrieves the associated user and their role
    information. It returns a profile response containing the profile details, user information,
    and role associated with the user.

    Args:
        db (Session): The database session to interact with the database.
        id (int): The ID of the profile to retrieve.

    Returns:
        ProfileSchemaResponse: A response containing the profile details along with the associated user
                               and role information.

    Raises:
        HTTPException: If the profile is not found, a 404 HTTPException is raised with the message
                        "Profile not found".
    """
    profile = profile_service.get_profile(db, profile_id)
    if profile:
        user = user_service.get_user(db, profile.user_id)
        role = role_service.get_role_by_id(db, user.role_id)
        role = RoleSchemaResponse(
            id=role.id,
            role=role.role
        )
        user = UserResponse(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            is_planner=user.is_planner,
            role=role,
            account_id=user.account_id
        )
        return ProfileSchemaResponse(
            id=profile.id,
            first_name=profile.first_name,
            last_name=profile.last_name,
            photo=profile.photo,
            nb_like=profile.nb_like,
            user=user,
            created_at=profile.created_at,
            updated_at=profile.updated_at
            )
    raise HTTPException(status_code=404, detail="Profile not found")

def update_profile(db: Session, profile_schema: ModifyProfileSchema, profile_id: int) -> ProfileSchemaResponse:
    """
    Updates a user's profile and associated user details.

    This function updates the user's profile and user details by ID. It updates the user information
    such as email, phone number, and planner status, and then updates the profile's first name, last name,
    photo, and like count. It also logs the update action and returns the updated profile details.

    Args:
        db (Session): The database session to interact with the database.
        profile (ProfileSchema): The profile information to update.
        id (int): The ID of the profile to update.

    Returns:
        ProfileSchemaResponse: A response containing the updated profile details, user information, and role.
    """
    user = user_service.update_user_phone_number(
        db,
        profile_id,
        profile_schema.phone_number
    )
    profile = profile_service.update_profile_personal_infos(
        db,
        profile_id,
        profile_schema.first_name,
        profile_schema.last_name,
        profile_schema.photo
    )
    role = role_service.get_role_by_id(db, user.role_id)
    role = RoleSchemaResponse(
        id=role.id,
        role=role.role
    )

    action_log_service.create_action_log(
        db,
        user.id,
        LogLevelEnum.INFO,
        ActionEnum.PROFILE_UPDATED,
        f"Profile {profile.id} updated at {profile.updated_at} by {user.email}"
    )

    return ProfileSchemaResponse(
        id=profile.id,
        first_name=profile.first_name,
        last_name=profile.last_name,
        photo=profile.photo,
        nb_like=profile.nb_like,
        user=UserResponse(
                id=user.id,
                email=user.email,
                phone_number=user.phone_number,
                is_planner=user.is_planner,
                role=role,
                account_id=user.account_id
            ),
        created_at=profile.created_at,
        updated_at=profile.updated_at
        )

def delete_profile(db: Session, profile_id: int, current_user_id: int) -> dict[str, str]:
    """
    Deletes a user profile from the system.

    This function deletes a user profile by ID. The profile can only be deleted by a user with
    appropriate privileges (typically an admin). It performs the deletion by invoking a service
    that handles the removal of the user from the database.

    Args:
        db (Session): The database session to interact with the database.
        profile_id (int): The ID of the profile to delete.
        current_user_id (int): The ID of the current user requesting the deletion.

    Returns:
        dict: A dictionary with a message confirming the deletion of the profile.
    """
    moderation_service.delete_user(db, profile_id, current_user_id)
    return {"msg": "supprime"}

def filter_profiles(
    db: Session,
    nb_like: Optional[int],
    is_planner: Optional[bool],
    role: Optional[RoleEnum],
    search: Optional[str],
    offset: int,
    limit: int
) -> ProfileListSchemaResponse:
    """
    Filters profiles based on the provided criteria.

    Args:
        db (Session): The database session used to interact with the database.
        nb_like (Optional[int]): The minimum number of likes a profile must have.
        is_planner (Optional[bool]): A flag indicating if the user is a planner.
        role (Optional[RoleEnum]): The role of the user (e.g., ADMIN, USER).
        search (Optional[str]): A search string to match the profiles (can match on first name, last name, or email).
        offset (int): The offset for pagination, determining the starting index of the profiles to retrieve.
        limit (int): The maximum number of profiles to retrieve.

    Returns:
        ProfileListSchemaResponse: A response containing the list of profiles matching the given criteria.
            The response includes:
                - count: The total number of profiles matching the criteria.
                - data: A list of ProfileSchemaResponse objects representing the filtered profiles.
    """
    profiles =  profile_service.get_profiles_by_filters(db, nb_like, is_planner, role, search, offset, limit)
    total = profile_service.get_profiles_by_filters_total_count(db, nb_like, is_planner, role, search)

    all_profiles = []
    for profile in profiles:
        user = user_service.get_user(db, profile.user_id)
        role = role_service.get_role_by_id(db, user.role_id)
        role_schema = RoleSchemaResponse(
            id=role.id,
            role=role.role
        )
        user = UserResponse(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            is_planner=user.is_planner,
            role=role_schema,
            account_id=user.account_id
        )

        all_profiles.append(
            ProfileSchemaResponse(
                id=profile.id,
                first_name=profile.first_name,
                last_name=profile.last_name,
                photo=profile.photo,
                nb_like=profile.nb_like,
                user=user,
                created_at=profile.created_at,
                updated_at=profile.updated_at
            )
        )
        
    return ProfileListSchemaResponse(
        count=len(all_profiles),
        total=total,
        data=all_profiles
    )


def filter_profiles_restricted(
    db: Session,
    nb_like: Optional[int],
    role: Optional[RoleEnum],
    search: Optional[str],
    offset: int,
    limit: int
) -> ProfileRestrictedListSchemaResponse:
    """
    Filters restricted profiles based on the provided criteria. This function is meant for fetching profiles
    where the user is a planner (i.e., `is_planner` is set to `True`).

    Args:
        db (Session): The database session used to interact with the database.
        nb_like (Optional[int]): The minimum number of likes a profile must have.
        role (Optional[RoleEnum]): The role of the user (e.g., ADMIN, USER).
        search (Optional[str]): A search string to match the profiles (can match on first name, last name, or email).
        offset (int): The offset for pagination, determining the starting index of the profiles to retrieve.
        limit (int): The maximum number of profiles to retrieve.

    Returns:
        ProfileRestrictedListSchemaResponse: A response containing the list of restricted profiles matching the given criteria.
            The response includes:
                - count: The total number of profiles matching the criteria.
                - data: A list of ProfileRestrictedSchemaResponse objects representing the filtered profiles with restricted data.
    """
    profiles =  profile_service.get_profiles_by_filters(db, nb_like, True, role, search, offset, limit)

    all_profiles = []
    for profile in profiles:
        user = user_service.get_user(db, profile.user_id)
        all_profiles.append(
            ProfileRestrictedSchemaResponse(
                id=profile.id,
                first_name=profile.first_name,
                last_name=profile.last_name,
                photo=profile.photo,
                nb_like=profile.nb_like,
                email=user.email,
                created_at=profile.created_at,
            )
        )
    return ProfileRestrictedListSchemaResponse(
        count=len(all_profiles),
        data=all_profiles
    )

def get_admins(db: Session) -> ProfileListSchemaResponse:
    """
    Retrieves a list of all profiles with admin roles from the database.

    Args:
        db (Session): The database session used to interact with the database.

    Returns:
        ProfileListSchemaResponse: A response containing a list of profiles with admin roles.
            The response includes:
                - count: The total number of admin profiles found.
                - data: A list of ProfileSchemaResponse objects representing the admin profiles.
    """
    profiles = profile_service.get_admins(db)
    all_profiles = []
    for profile in profiles:
        user = user_service.get_user(db, profile.user_id)
        role = role_service.get_role_by_id(db, user.role_id)
        role = RoleSchemaResponse(
            id=role.id,
            role=role.role
        )
        user = UserResponse(
            id=user.id,
            email=user.email,
            phone_number=user.phone_number,
            is_planner=user.is_planner,
            role=role,
            account_id=user.account_id
        )

        all_profiles.append(
            ProfileSchemaResponse(
                id=profile.id,
                first_name=profile.first_name,
                last_name=profile.last_name,
                photo=profile.photo,
                nb_like=profile.nb_like,
                user=user,
                created_at=profile.created_at,
                updated_at=profile.updated_at
            )
        )

    return ProfileListSchemaResponse(
        count=len(all_profiles),
        data=all_profiles
    )
