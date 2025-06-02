from datetime import datetime
from typing import Optional
from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from controllers import authent_controller, signaled_comment_controller
from database.db import get_db
from schemas.request_schemas.signaled_comment_schema import SignaledCommentByCurrentUserSchema
from schemas.response_schemas.signaled_comment_schema_response import SignaledCommentSchemaResponse, SignaledCommentListSchemaResponse
from models.user_model import User


router = APIRouter(
    prefix="/api/v1/signaledComments",
    tags=["signaledComment"],
)

# 1. Création (POST)
@router.post("/", response_model=bool, status_code=201)
def signal_comment(
    signaled_comment: SignaledCommentByCurrentUserSchema,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> bool:
    """Allows the current user to signal a comment. Returns a boolean indicating success."""
    return signaled_comment_controller.create_signaled_comment_by_current_user(db, signaled_comment, current_user)


# 3. Liste filtrée (GET)
@router.get("/", response_model=SignaledCommentListSchemaResponse, status_code=200)
def get_signaled_comments_by_filters(
    date: datetime = Query(None),
    user_id: int = Query(None),
    email_user: str = Query(None),
    reason_id: int = Query(None),
    comment_id: int = Query(None),
    status: str = Query(None),
    offset: int = Query(0),
    limit: int = Query(5),
    email_comment_user: str = Query(None),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> SignaledCommentListSchemaResponse:
    """Retrieve a filtered list of signaled comments, with optional filters like date, user ID, reason, status, etc.
    Accessible to admin or super-admin only."""
    return signaled_comment_controller.get_signaled_comments_filters(
        db,
        date,
        user_id,
        reason_id,
        comment_id,
        status,
        email_user,
        email_comment_user,
        offset,
        limit
    )


# 4. Mise à jour (PATCH)
@router.patch("/{signaled_comment_id}", response_model=SignaledCommentSchemaResponse, status_code=200)
def update_status_signaled_comment(
    signaled_comment_id: int,
    status: str = Query(None),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> SignaledCommentSchemaResponse:
    """Update the status of a signaled comment (e.g., mark as resolved, dismissed). Accessible to admin or super-admin only."""
    return signaled_comment_controller.update_signaled_comment_status(db, signaled_comment_id, status)


# 5. Suppression (DELETE)
@router.delete("/{signaled_comment_id}", response_model=dict[str, str], status_code=200)
def delete_signaled_comment(
    signaled_comment_id: int,
    ban: Optional[bool] = False,
    current_user: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> dict[str, str]:
    """Delete a signaled comment. Optionally ban the user responsible for the comment. Accessible to admin or super-admin only."""
    return signaled_comment_controller.delete_signaled_comment(db, signaled_comment_id, ban, current_user)
