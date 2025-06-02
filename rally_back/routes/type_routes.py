from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from database.db import get_db
from controllers import authent_controller, type_controller
from schemas.response_schemas.type_schema_response import TypeSchemaResponse, TypeListSchemaResponse
from models.user_model import User


router = APIRouter(
    prefix="/api/v1/types",
    tags=["types"],
)

@router.get("/", response_model=TypeListSchemaResponse, status_code=200)
def get_types(
    db: Session = Depends(get_db)
) -> TypeListSchemaResponse:
    """Retrieve a list of all available types (e.g., event types). Accessible by any connected user."""
    return type_controller.get_types(db)


@router.get("/{type_id}", response_model=TypeSchemaResponse, status_code=200)
def get_type_by_id(
    type_id: int,
    _: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> TypeSchemaResponse:
    """Retrieve a specific type by its ID. Accessible by any connected user."""
    return type_controller.get_type_by_id(db, type_id)


@router.delete("/{type_id}", response_model=dict[str, str], status_code=200)
def delete_type(
    type_id: int,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> TypeSchemaResponse:
    """Delete a type by its ID. Accessible by any connected user. The action may be restricted based on the user's role."""
    return type_controller.delete_type(db, type_id, current_user)
