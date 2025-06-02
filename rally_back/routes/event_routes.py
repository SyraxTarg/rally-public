from datetime import datetime
from fastapi import Depends, APIRouter, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from controllers import authent_controller
from database.db import get_db
from models.user_model import User
from controllers import event_controller
from schemas.request_schemas.event_schema import EventSchema
from schemas.response_schemas.event_schema_response import EventSchemaResponse, EventListSchemaResponse

router = APIRouter(
    prefix="/api/v1/events",
    tags=["events"],
)

@router.post("/", response_model=EventSchemaResponse, status_code=201)
def post_event(
    event: EventSchema,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> EventSchemaResponse:
    """Create a new event (connected user required)."""
    return event_controller.create_event(db, event, current_user)

@router.get("/", response_model=EventListSchemaResponse, status_code=200)
def get_events(
    date_avant: datetime = Query(None),
    date_apres: datetime = Query(None),
    type_ids: list[int] = Query(None),
    profile_id: int = Query(None),
    country: str = Query(None),
    city: str = Query(None),
    popularity: bool = Query(None),
    recent: bool = Query(None),
    nb_places: int = Query(None),
    search: str = Query(None),
    offset: int = Query(0),
    limit: int = Query(5),
    db: Session = Depends(get_db)
) -> EventListSchemaResponse:
    """Retrieve a filtered and paginated list of events."""
    return event_controller.get_events(
        db,
        date_avant,
        date_apres,
        type_ids,
        profile_id,
        country,
        city,
        popularity,
        recent,
        nb_places,
        search,
        offset,
        limit
    )

@router.get("/{event_id}", response_model=EventSchemaResponse, status_code=200)
def get_event(
    event_id: int,
    db: Session = Depends(get_db)
) -> EventSchemaResponse:
    """Retrieve event details by event ID."""
    return event_controller.get_event_by_id(db, event_id)

@router.patch("/{event_id}", response_model=EventSchemaResponse, status_code=200)
def update_event(
    event_id: int,
    event: EventSchema,
    _: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> EventSchemaResponse:
    """Update an existing event (event owner required)."""
    return event_controller.update_event(db, event_id, event)

@router.delete("/{event_id}", response_model=dict[str, str], status_code=200)
def delete_event(
    event_id: int,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> JSONResponse:
    """Delete an event by ID (only by its owner)."""
    return event_controller.delete_event(db, event_id, current_user)

@router.get("/profiles/{event_id}", response_model=EventListSchemaResponse, status_code=200)
def get_events_by_profile(
    event_id: int,
    offset: int = Query(0),
    limit: int = Query(5),
    db: Session = Depends(get_db)
) -> EventListSchemaResponse:
    """Get all events created by a specific profile (paginated)."""
    return event_controller.get_events_by_profile(
        db,
        event_id,
        offset,
        limit
    )
