from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session
from controllers import authent_controller
from database.db import get_db
from schemas.request_schemas.user_schema import UserSchema
from schemas.response_schemas.user_schema_response import UserResponse, UserListResponse
from controllers import user_controller
from models.user_model import User


router = APIRouter(
    prefix="/api/v1/users",
    tags=["user"],
)

# 📌 1️⃣ Récupérer un utilisateur par ID
@router.get("/{user_id}", response_model=UserResponse, status_code=200)
def get_user(
    user_id: int,
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> UserResponse:
    """Retrieve a user by their ID. Accessible by an admin or super admin."""
    return user_controller.get_user(db, user_id)


# 📌 3️⃣ Rechercher des utilisateurs par email
@router.get("/", response_model=UserListResponse, status_code=200)
def search_users(
    offset: int = Query(0),
    limit: int = Query(5),
    search: str = Query(None, description="Search for users by email."),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> UserListResponse:
    """Search for users by their email. Accessible by an admin or super admin."""
    return user_controller.search_users(db, search, offset, limit)


# 📌 5️⃣ Mettre à jour un utilisateur
@router.patch("/{user_id}", response_model=UserResponse, status_code=201)
def update_user(
    user_id: int,
    user: UserSchema,
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> UserResponse:
    """Update a user's details. Accessible by an admin or super admin."""
    return user_controller.update_user(db, user, user_id)


# 📌 6️⃣ Activer/Désactiver "is_planner"
@router.patch("/toggle/{user_id}", response_model=UserResponse, status_code=201)
def toggle_user_planner(
    user_id: int,
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> UserResponse:
    """Toggle the 'is_planner' status of a user. Accessible by an admin or super admin."""
    return user_controller.toggle_is_planner(db, user_id)


# 📌 7️⃣ Supprimer un utilisateur
@router.delete("/{user_id}", response_model=dict[str, str], status_code=201)
def ban_user(
    user_id: int,
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> dict[str, str]:
    """Delete or ban a user by their ID. Accessible by an admin or super admin."""
    return user_controller.delete_user(db, user_id)
