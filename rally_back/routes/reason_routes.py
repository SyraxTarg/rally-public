from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session

from controllers import authent_controller, reason_controller
from database.db import get_db
from schemas.response_schemas.reason_schema_response import ReasonSchemaResponse, ReasonListSchemaResponse
from models.user_model import User

router = APIRouter(
    prefix="/api/v1/reasons",
    tags=["reason"],
)

@router.get("/", response_model=ReasonListSchemaResponse, status_code=200)
def get_reasons(
    db: Session = Depends(get_db)
) -> ReasonListSchemaResponse:
    """Get a list of reasons with pagination. Accessible to admin or super-admin."""
    return reason_controller.get_reasons(db)

@router.get("/{reason_id}", response_model=ReasonSchemaResponse, status_code=200)
def get_reason(
    reason_id: int,
    _: User = Depends(authent_controller.get_current_admin_or_super_admin),
    db: Session = Depends(get_db)
) -> ReasonSchemaResponse:
    """Get a specific reason by its ID. Accessible to admin or super-admin."""
    return reason_controller.get_reason_by_id(db, reason_id)

@router.delete("/{reason_id}", response_model=dict[str, str], status_code=200)
def delete_reason(
    reason_id: int,
    current_user: User = Depends(authent_controller.get_current_super_admin),
    db: Session = Depends(get_db)
) -> dict[str, str]:
    """Delete a specific reason by its ID. Accessible only to super-admin."""
    return reason_controller.delete_reason(db, reason_id, current_user)
