from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session
from controllers import authent_controller
from database.db import get_db
from models.user_model import User
from controllers import comment_controller
from schemas.request_schemas.comment_schema import CommentSchema
from schemas.response_schemas.comment_schema_response import CommentSchemaResponse, CommentListSchemaResponse

router = APIRouter(
    prefix="/api/v1/comments",
    tags=["comment"],
)

@router.get("/events/{event_id}", response_model=CommentListSchemaResponse, status_code=200)
def get_comments_from_event(
    event_id: int,
    offset: int = Query(0),
    limit: int = Query(5),
    db: Session = Depends(get_db)
) -> CommentListSchemaResponse:
    """Get comments posted on a specific event (connected users only)."""
    return comment_controller.get_comments_from_event(db, event_id, offset, limit)

@router.get("/profiles/{profile_id}", response_model=CommentListSchemaResponse, status_code=200)
def get_comments_from_profile(
    profile_id: int,
    offset: int = Query(0),
    limit: int = Query(5),
    _: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> CommentListSchemaResponse:
    """Get comments made by a specific profile (connected users only)."""
    return comment_controller.get_comments_from_profile(db, profile_id, offset, limit)

@router.get("/", response_model=CommentListSchemaResponse, status_code=200)
def get_comments(
    offset: int = Query(0),
    limit: int = Query(5),
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> CommentListSchemaResponse:
    """Retrieve all comments (admin/super-admin only, paginated)."""
    return comment_controller.get_comments(db, offset, limit)

@router.get("/{id}", response_model=CommentSchemaResponse, status_code=200)
def get_comment_by_id(
    comment_id: int,
    _: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> CommentSchemaResponse:
    """Retrieve a comment by its ID (connected users only)."""
    return comment_controller.get_comment_by_id(db, comment_id)

@router.post("/", response_model=CommentSchemaResponse, status_code=201)
def comment_event(
    comment: CommentSchema,
    current_user: User = Depends(authent_controller.get_current_user),
    db: Session = Depends(get_db)
) -> CommentSchemaResponse:
    """Post a comment on an event (authenticated user required)."""
    return comment_controller.comment_event(db, comment, current_user.id)

@router.delete("/{comment_id}", response_model=dict[str, str], status_code=200)
def delete_comment(
    comment_id: int,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> CommentSchemaResponse:
    """Delete a comment by ID (only by its author)."""
    return comment_controller.delete_comment(db, comment_id, current_user.id)
