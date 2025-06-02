from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from database.db import get_db
from controllers import authent_controller
from controllers import profile_controller
from models.user_model import User
from schemas.request_schemas.profile_schema import ProfileSchema, ModifyProfileSchema
from schemas.response_schemas.profile_schema_response import ProfileSchemaResponse, ProfileListSchemaResponse, ProfileRestrictedListSchemaResponse
from enums.role import RoleEnum

router = APIRouter(
    prefix="/api/v1/profiles",
    tags=["profile"],
)

@router.get("/me", response_model=ProfileSchemaResponse, status_code=200)
def get_current_profile(
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> ProfileSchemaResponse:
    """Get the profile of the currently authenticated user."""
    return profile_controller.get_profile(db, current_user.id)

@router.get("/", response_model=ProfileListSchemaResponse, status_code=200)
def filter_profiles(
    nb_like: str = Query(None),
    is_planner: bool = Query(None),
    role: RoleEnum = Query(None),
    search: str = Query(None),
    offset: int = Query(0),
    limit: int = Query(5),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> ProfileListSchemaResponse:
    """Get a list of profiles with optional filters (likes, role, search). Accessible to admin or super-admin."""
    return profile_controller.filter_profiles(db, nb_like, is_planner, role, search, offset, limit)

@router.get("/{profile_id}", response_model=ProfileSchemaResponse, status_code=200)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db)
) -> ProfileSchemaResponse:
    """Get the profile of a specific user by their profile ID."""
    return profile_controller.get_profile(db, profile_id)

@router.patch("/", response_model=ProfileSchemaResponse, status_code=200)
def update_profile(
    profile: ModifyProfileSchema,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> ProfileSchemaResponse:
    """Update the profile of the currently authenticated user."""
    return profile_controller.update_profile(db, profile, current_user.id)

@router.delete("/{profile_id}", response_model=dict[str, str], status_code=200)
def delete_profile(
    profile_id: int,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> dict[str, str]:
    """Delete the profile of a user by their profile ID."""
    return profile_controller.delete_profile(db, profile_id, current_user.id)
