from datetime import datetime
from typing import Optional
from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from controllers import authent_controller, signaled_event_controller
from database.db import get_db
from schemas.request_schemas.signaled_event_schema import SignaledEventByCurrentUserSchema
from schemas.response_schemas.signaled_event_schema_response import SignaledEventSchemaResponse, SignaledEventListSchemaResponse
from models.user_model import User


router = APIRouter(
    prefix="/api/v1/signaledEvents",
    tags=["signaledEvent"],
)

# 1. Création (POST)
@router.post("/", response_model=bool, status_code=201)
def signal_event(
    signaled_event: SignaledEventByCurrentUserSchema,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> bool:
    """Allows the current user to signal an event. Returns a boolean indicating success."""
    return signaled_event_controller.create_signaled_event_by_current_user(db, signaled_event, current_user)


# 2. Liste avec filtres (GET /)
@router.get("/", response_model=SignaledEventListSchemaResponse, status_code=200)
def get_signaled_events_by_filters(
    date: datetime = Query(None),
    user_id: int = Query(None),
    email_user: str = Query(None),
    email_event_user: str = Query(None),
    reason_id: int = Query(None),
    event_id: int = Query(None),
    status: str = Query(None),
    offset: int = Query(0),
    limit: int = Query(5),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> SignaledEventListSchemaResponse:
    """Retrieve a filtered list of signaled events based on various criteria (e.g., date, user ID, reason, status).
    Accessible to admin or super-admin only."""
    return signaled_event_controller.get_signaled_events_filters(
        db,
        date,
        user_id,
        reason_id,
        event_id,
        status,
        email_user,
        email_event_user,
        offset,
        limit
    )


# 3. Récupération par ID (GET /{id})
@router.get("/{signaled_event_id}", response_model=SignaledEventSchemaResponse, status_code=200)
def get_signaled_event_by_id(
    signaled_event_id: int,
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> SignaledEventSchemaResponse:
    """Retrieve the details of a specific signaled event by its ID. Accessible to admin or super-admin only."""
    return signaled_event_controller.get_signaled_event_by_id(db, signaled_event_id)


# 4. Mise à jour (PATCH /{id})
@router.patch("/{signaled_event_id}", response_model=SignaledEventSchemaResponse, status_code=200)
def update_status_signaled_event(
    signaled_event_id: int,
    status: str = Query(None),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> SignaledEventSchemaResponse:
    """Update the status of a signaled event (e.g., mark as resolved, dismissed). Accessible to admin or super-admin only."""
    return signaled_event_controller.update_signaled_event_status(db, signaled_event_id, status)


# 5. Suppression (DELETE /{id})
@router.delete("/{signaled_event_id}", response_model=dict[str, str], status_code=200)
def delete_signaled_event(
    signaled_event_id: int,
    ban: Optional[bool] = False,
    current_user: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> dict[str, str]:
    """Delete a signaled event. Optionally ban the user responsible for the event. Accessible to admin or super-admin only."""
    return signaled_event_controller.delete_signaled_event(db, signaled_event_id, current_user, ban)
