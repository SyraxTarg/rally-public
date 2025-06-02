"""
This file contains the controller related to types
"""
from datetime import datetime
from sqlalchemy.orm import Session
from services import action_log_service, type_service
from schemas.request_schemas.type_schema import TypeSchema
from schemas.response_schemas.type_schema_response import TypeSchemaResponse, TypeListSchemaResponse
from enums.log_level import LogLevelEnum
from enums.action import ActionEnum
from models.user_model import User


def create_type(db: Session, type_: TypeSchema, current_user: User) -> TypeSchemaResponse:
    """
    Creates a new event type in the system and logs the action performed by the current user.

    This function allows an admin or authorized user to create a new event type, which can
    later be associated with events in the application. The action is logged for auditing purposes.

    Args:
        db (Session): The database session used to interact with the database.
        type_ (TypeSchema): A schema object containing the details of the new event type,
            including the name of the type.
        current_user (User): The user who is performing the action of creating the new event type.
            This user will be recorded in the action log.

    Returns:
        TypeSchemaResponse: A response object containing the ID and name of the newly created event type.
    """
    new_type = type_service.create_type(db, type_.type)

    action_log_service.create_action_log(
        db,
        current_user.id,
        LogLevelEnum.INFO,
        ActionEnum.TYPE_CREATED,
        f"User {current_user.id} added type {new_type.id} at {datetime.now()} by {current_user.email}"
    )

    return TypeSchemaResponse(
        id=new_type.id,
        type=new_type.type
    )

def get_type_by_id(db: Session, type_id: int) -> TypeSchemaResponse:
    """
    Retrieves an event type from the database by its ID.

    This function fetches a specific event type using its unique identifier
    and returns it as a response object.

    Args:
        db (Session): The database session used to interact with the database.
        type_id (int): The unique identifier (ID) of the event type to retrieve.

    Returns:
        TypeSchemaResponse: A response object containing the ID and name of the event type.
    """
    type_ = type_service.get_type_by_id(db, type_id)
    return TypeSchemaResponse(
        id=type_.id,
        type=type_.type
    )

def get_types(db: Session) -> TypeListSchemaResponse:
    """
    Retrieves all event types from the database.

    This function fetches a list of all available event types and returns
    them as a response object containing a count and a list of types.

    Args:
        db (Session): The database session used to interact with the database.

    Returns:
        TypeListSchemaResponse: A response object containing the count of event types
        and a list of event types with their IDs and names.
    """
    types = type_service.get_types(db)

    all_types = []

    for type_ in types:
        all_types.append(
            TypeSchemaResponse(
                id=type_.id,
                type=type_.type
            )
        )

    return TypeListSchemaResponse(
        count=len(all_types),
        data=all_types
    )


def delete_type(db: Session, type_id: int, current_user: User) -> dict[str, str]:
    """
    Deletes an event type from the database.

    This function removes an event type identified by its `id` from the database
    and logs the action performed by the current user in the action log.

    Args:
        db (Session): The database session used to interact with the database.
        type_id (int): The ID of the event type to be deleted.
        current_user (User): The user performing the deletion.

    Returns:
        dict: A dictionary containing a message indicating the deletion status.
    """
    type_service.delete_type(db, type_id)

    action_log_service.create_action_log(
        db,
        current_user.id,
        LogLevelEnum.INFO,
        ActionEnum.TYPE_DELETED,
        f"User {current_user.id} deleted type {type_id} at {datetime.now()} by {current_user.email}"
    )

    return {"msg": "deleted"}
