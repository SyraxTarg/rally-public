"""
This file contains the controller related to users
"""
from typing import Optional
from sqlalchemy.orm import Session
from enums.role import RoleEnum
from schemas.request_schemas.user_schema import UserSchema
from schemas.response_schemas.user_schema_response import UserResponse, UserListResponse
from schemas.response_schemas.role_schema_response import RoleSchemaResponse
from services import moderation_service, role_service, user_service

def get_user(db: Session, user_id: int) -> UserResponse:
    """
    Retrieves a user by their ID from the database.

    This function fetches a user and their role from the database using the provided ID,
    and returns the user information in a structured response format.

    Args:
        db (Session): The database session used to interact with the database.
        user_id (int): The ID of the user to retrieve.

    Returns:
        UserResponse: A response object containing the user's details including their role.
    """
    user = user_service.get_user(db, user_id)
    role = role_service.get_role_by_id(db, user.role_id)
    return UserResponse(
        id=user.id,
        email=user.email,
        phone_number=user.phone_number,
        is_planner=user.is_planner,
        role=RoleSchemaResponse(
            id=role.id,
        ),
        account_id=user.account_id
    )

def update_user(db: Session, user: UserSchema, user_id: int) -> UserResponse:
    """
    Updates a user's details in the database based on the provided user schema.

    This function updates a user's email, phone number, and planner status in the database.
    It also retrieves and includes the user's role information in the response.

    Args:
        db (Session): The database session used to interact with the database.
        user (UserSchema): The updated user data, including email, phone number, and planner status.
        id (int): The ID of the user to update.

    Returns:
        UserResponse: A response object containing the updated user details, including their role.
    """
    user = user_service.update_user(
        db,
        user_id,
        user.email,
        user.phone_number,
        user.is_planner
    )
    role = role_service.get_role_by_id(db, user.role_id)
    return UserResponse(
        id=user.id,
        email=user.email,
        phone_number=user.phone_number,
        is_planner=user.is_planner,
        role=RoleSchemaResponse(
            id=role.id,
            role=role.role
        ),
        account_id=user.account_id
    )

def delete_user(db: Session, user_id: int) -> dict[str, str]:
    """
    Deletes a user from the database.

    This function deletes a user by their ID. The deletion is performed using a moderation service.
    After the deletion, a success message is returned indicating the user has been reported.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): The ID of the user to delete.

    Returns:
        dict[str, str]: A dictionary with a message indicating that the user has been reported.
    """
    moderation_service.delete_user(db, user_id)
    return {"msg": "le user a  été signalé"}

def search_users(db: Session, search: Optional[str], offset: int, limit: int) -> UserListResponse:
    """
    Searches for users based on the provided search term and pagination parameters.

    This function retrieves a list of users that match the search term, with pagination support
    for large datasets. The users' roles are also fetched and included in the response.

    Args:
        db (Session): The database session used to interact with the database.
        search (Optional[str]): The search term used to filter users. If `None`, all users are fetched.
        offset (int): The number of items to skip before starting to return results (used for pagination).
        limit (int): The maximum number of users to return (used for pagination).

    Returns:
        UserListResponse: A response object containing the total count of matching users and the list of users.
            - `count`: Total number of users that match the search criteria.
            - `data`: A list of users with their roles, email, phone number, and planner status.
    """
    users = user_service.search_users(db, search, offset, limit)

    all_users = []
    for user in users:
        role = role_service.get_role_by_id(db, user.role_id)
        all_users.append(
            UserResponse(
                id=user.id,
                email=user.email,
                phone_number=user.phone_number,
                is_planner=user.is_planner,
                role=RoleSchemaResponse(
                    id=role.id,
                    role=role.role
                ),
                account_id=user.account_id
            )
        )
    return UserListResponse(
        count=len(all_users),
        data=all_users
    )

def toggle_is_planner(db: Session, user_id: int) -> UserResponse:
    """
    Toggles the 'is_planner' status of a user.

    This function changes the 'is_planner' attribute of a user to the opposite of its current value
    (i.e., if the user is a planner, it will be set to `False`, and if the user is not a planner,
    it will be set to `True`). The user's role is also fetched and included in the response.

    Args:
        db (Session): The database session used to interact with the database.
        id (int): The ID of the user whose 'is_planner' status is to be toggled.

    Returns:
        UserResponse: A response object containing the updated user information:
            - `id`: The ID of the user.
            - `email`: The email of the user.
            - `phone_number`: The phone number of the user.
            - `is_planner`: The updated planner status of the user (True or False).
            - `role`: The role of the user, including the role ID and name.
    """
    user = user_service.toggle_is_planner(db, user_id)
    role = role_service.get_role_by_id(db, user.role_id)
    return UserResponse(
        id=user.id,
        email=user.email,
        phone_number=user.phone_number,
        is_planner=user.is_planner,
        role=RoleSchemaResponse(
            id=role.id,
            role=role.role
        ),
        account_id=user.account_id
    )

def grant_priviledges(db: Session, user_id: int, role: RoleEnum) -> UserResponse:
    """
    Grants a specified role to a user.

    This function assigns a new role to a user identified by their ID. If the user exists, the specified role
    from the `RoleEnum` is assigned to the user. The updated user details, including the role, are then returned.

    Args:
        db (Session): The database session used to interact with the database.
        user_id (int): The ID of the user to whom the role will be granted.
        role (RoleEnum): The role to be assigned to the user. The role should be a valid member of `RoleEnum`.

    Returns:
        UserResponse: A response object containing the updated user information:
            - `id`: The ID of the user.
            - `email`: The email of the user.
            - `phone_number`: The phone number of the user.
            - `is_planner`: The planner status of the user (True or False).
            - `role`: The new role of the user, including the role ID and name.
    """
    user = user_service.get_user(db, user_id)
    if user:
        role_to_grant = role_service.get_role(db, role)
        user = user_service.grant_role(db, role_to_grant, user)
        return UserResponse(
        id=user.id,
        email=user.email,
        phone_number=user.phone_number,
        is_planner=user.is_planner,
        role=RoleSchemaResponse(
            id=role_to_grant.id,
            role=role_to_grant.role
        ),
        account_id=user.account_id
    )
    return None
