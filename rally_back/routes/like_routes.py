from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from controllers import authent_controller
from database.db import get_db
from models.user_model import User
from controllers import like_controller
from schemas.response_schemas.like_schema_response import LikeSchemaresponseSchemas,  LikeListSchemaresponseSchemas, IsLikedResponseSchema

router = APIRouter(
    prefix="/api/v1/likes",
    tags=["like"],
)

@router.delete("/{event_id}", response_model=dict[str, str], status_code=200)
def unlike_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(authent_controller.get_connected_user)
) -> dict[str, str]:
    """Remove a like from an event for the current user."""
    return like_controller.unlike_event(db, current_user.id, event_id)

@router.get("/", response_model= LikeListSchemaresponseSchemas, status_code=200)
def get_likes(
    offset: int = Query(0),
    limit: int = Query(5),
    db: Session = Depends(get_db),
    _: User = Depends(authent_controller.get_connected_user)
) ->  LikeListSchemaresponseSchemas:
    """Get a paginated list of all likes (admin or authenticated users)."""
    return like_controller.get_likes(db, offset, limit)

@router.post("/{event_id}", response_model=LikeSchemaresponseSchemas, status_code=200)
def like_event(
    event_id: int,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> LikeSchemaresponseSchemas:
    """Like an event as the current user."""
    return like_controller.like_event_current_user(db, current_user.id, event_id)

@router.get("/is_liked", response_model=IsLikedResponseSchema, status_code=200)
def is_event_liked_by(
    event_id: int = Query,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> IsLikedResponseSchema:
    """Check if the current user has liked a specific event."""
    return like_controller.is_event_liked_by_current(db, event_id, current_user.id)
