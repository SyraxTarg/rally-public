from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from controllers import authent_controller
from database.db import get_db
from models.user_model import User
from controllers import banned_users_controller
from schemas.response_schemas.banned_user_schema_response import BannedUserListSchemaResponse, BannedUserSchemaResponse

router = APIRouter(
    prefix="/api/v1/bannedUsers",
    tags=["banned_users"],
)

@router.get("/", response_model=BannedUserListSchemaResponse, status_code=200)
def get_banned_users(
    offset: int = Query(0),
    limit: int = Query(5),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> BannedUserListSchemaResponse:
    """Get a paginated list of banned users (admin/super-admin only)."""
    return banned_users_controller.get_banned_users(db, offset, limit)

@router.get("/by-email", response_model=BannedUserSchemaResponse, status_code=200)
def get_banned_user_by_email(
    email: str = Query,
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> BannedUserSchemaResponse:
    """Retrieve details of a banned user by email (admin/super-admin only)."""
    return banned_users_controller.get_banned_user_by_email(db, email)

@router.delete("/", response_model=bool, status_code=200)
def delete_banned_user_by_email(
    email: str = Query,
    current_user: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> bool:
    """Unban a user by email (admin/super-admin only)."""
    return banned_users_controller.delete_banned_user(db, email, current_user)
