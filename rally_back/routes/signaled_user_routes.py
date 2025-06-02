from datetime import datetime
from typing import Optional
from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from controllers import authent_controller, signaled_user_controller
from database.db import get_db
from schemas.request_schemas.signaled_user_schema import SignaledUserCurrentUSerSchema
from schemas.response_schemas.signaled_user_schema_response import SignaledUserSchemaResponse, SignaledUserListSchemaResponse
from models.user_model import User


router = APIRouter(
    prefix="/api/v1/signaledUsers",
    tags=["signaledUser"],
)

# 🔹 3. Filtrer les signalements avec plusieurs critères
@router.get("/", response_model=SignaledUserListSchemaResponse, status_code=200)
def get_signaled_users_by_filters(
    date: datetime = Query(None),
    user_id: int = Query(None),
    email_user: str = Query(None),
    reason_id: int = Query(None),
    signaled_user_id: int = Query(None),
    email_signaled_user: str = Query(None),
    offset: int = Query(0),
    limit: int = Query(5),
    status: str = Query(None),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> SignaledUserListSchemaResponse:
    """Retrieve a filtered list of signaled users based on various criteria (e.g., date, user ID, reason, status).
    Accessible to admin or super-admin only."""
    return signaled_user_controller.get_signaled_user_by_filters(
        db,
        date,
        user_id,
        reason_id,
        signaled_user_id,
        status,
        email_user,
        email_signaled_user,
        offset,
        limit
    )


# 🔹 4. Créer un nouveau signalement
@router.post("/", response_model=bool, status_code=201)
def signal_user(
    signaled_user: SignaledUserCurrentUSerSchema,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> bool:
    """Allows the current user to signal another user. Returns a boolean indicating success."""
    return signaled_user_controller.create_signaled_user_by_current(db, signaled_user, current_user)


# 🔹 5. Mettre à jour le statut d'un signalement
@router.patch("/{signaled_user_id}", response_model=SignaledUserSchemaResponse, status_code=200)
def update_status_signaled_user(
    signaled_user_id: int,
    status: str = Query(None),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> SignaledUserSchemaResponse:
    """Update the status of a signal. (e.g., mark as resolved or dismissed). Accessible to admin or super-admin only."""
    return signaled_user_controller.update_status_signaled_user(db, signaled_user_id, status)


# 🔹 6. Supprimer un signalement
@router.delete("/{signaled_user_id}", response_model=dict[str, str], status_code=200)
def delete_signaled_user(
    signaled_user_id: int,
    ban: Optional[bool] = False,
    current_user: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> dict[str, str]:
    """Delete a signaled user. Optionally ban the user responsible for the violation. Accessible to admin or super-admin only."""
    return signaled_user_controller.delete_signaled_user(db, signaled_user_id, current_user, ban)
