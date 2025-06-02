from datetime import datetime
from fastapi import Depends, APIRouter, Query
from sqlalchemy.orm import Session
from controllers import (
    action_logs_controller,
    authent_controller,
    payment_controller,
    profile_controller,
    reason_controller,
    type_controller
)
from database.db import get_db
from schemas.response_schemas.user_schema_response import UserResponse
from schemas.response_schemas.profile_schema_response import ProfileListSchemaResponse
from controllers import user_controller
from schemas.response_schemas.action_log_schema_response import ActionLogListResponse
from schemas.response_schemas.type_schema_response import TypeListSchemaResponse
from models.user_model import User
from enums.role import RoleEnum
from enums.action import ActionEnum
from enums.log_level import LogLevelEnum
from schemas.response_schemas.type_schema_response import TypeSchemaResponse
from schemas.request_schemas.type_schema import TypeSchema
from schemas.request_schemas.reason_schema import ReasonSchema
from schemas.response_schemas.reason_schema_response import ReasonSchemaResponse
from enums.payment_status import PaymentStatusEnum
from schemas.response_schemas.payment_schema_response import PaymentListSchemaResponse



router = APIRouter(
    prefix="/api/v1/super-admin",
    tags=["super-admin"]
)

# 🔹 1. Accorder des privilèges à un utilisateur
@router.post("/user/{user_id}", response_model=UserResponse, status_code=201)
def grant_priviledges(
    user_id: int,
    role: RoleEnum = Query(None),
    _: User = Depends(authent_controller.get_current_super_admin),
    db: Session = Depends(get_db)
) -> UserResponse:
    """Grant specific privileges (role) to a user. This action is restricted to super-admins only."""
    return user_controller.grant_priviledges(db, user_id, role)


# 🔹 2. Filtrer les profils
@router.get("/profiles", response_model=ProfileListSchemaResponse, status_code=200)
def filter_profiles(
    nb_like: str = Query(None),
    is_planner: bool = Query(None),
    role: RoleEnum = Query(None),
    search: str = Query(None),
    offset: int = Query(0),
    limit: int = Query(5),
    _: User = Depends(authent_controller.get_current_super_admin),
    db: Session = Depends(get_db)
) -> ProfileListSchemaResponse:
    """Retrieve a filtered list of profiles based on various criteria (e.g., number of likes, role, planner status, search term)."""
    return profile_controller.filter_profiles(db, nb_like, is_planner, role, search, offset, limit)


# 🔹 3. Récupérer les logs d'action
@router.get("/logs", response_model=ActionLogListResponse, status_code=200)
def get_logs(
    date: datetime = Query(None),
    action_type: ActionEnum = Query(None),
    user_id: int = Query(None),
    log_type: LogLevelEnum = Query(None),
    offset: int = Query(0),
    limit: int = Query(5),
    _: User = Depends(authent_controller.get_current_super_admin),
    db: Session = Depends(get_db)
) -> ActionLogListResponse:
    """Fetch action logs with various filters, including date, action type, user ID, and log level. Restricted to super-admins."""
    return action_logs_controller.get_action_logs(db, date, action_type, user_id, log_type, offset, limit)


# 🔹 4. Créer un type
@router.post("/types", response_model=TypeSchemaResponse, status_code=201)
def create_type(
    type_schema: TypeSchema,
    current_user: User = Depends(authent_controller.get_current_super_admin),
    db: Session = Depends(get_db)
) -> TypeSchemaResponse:
    """Create a new type (e.g., event type, category). This is restricted to super-admins."""
    return type_controller.create_type(db, type_schema, current_user)


# 🔹 5. Créer une raison
@router.post("/reasons", response_model=ReasonSchemaResponse, status_code=201)
def create_reason(
    reason: ReasonSchema,
    current_user: User = Depends(authent_controller.get_current_super_admin),
    db: Session = Depends(get_db)
) -> ReasonSchemaResponse:
    """Create a new reason (e.g., reason for reporting, flagging). Restricted to super-admins."""
    return reason_controller.create_reason(db, reason, current_user)


# 🔹 6. Récupérer les paiements
@router.get("/payments", response_model=PaymentListSchemaResponse, status_code=200)
def get_payments(
    event_title: str = Query(None),
    buyer_email: str = Query(None),
    organizer_email: str = Query(None),
    amount_min: float = Query(None),
    amount_max: float = Query(None),
    fee_min: float = Query(None),
    fee_max: float = Query(None),
    brut_amount_min: float = Query(None),
    brut_amount_max: float = Query(None),
    stripe_session_id: str = Query(None),
    stripe_payment_intent_id: str = Query(None),
    status: PaymentStatusEnum = Query(None),
    date_apres: datetime = Query(None),
    date_avant: datetime = Query(None),
    offset: int = Query(0),
    limit: int = Query(5),
    _: User = Depends(authent_controller.get_current_super_admin),
    db: Session = Depends(get_db)
) -> PaymentListSchemaResponse:
    """Retrieve a list of payments with multiple filtering options (e.g., event, buyer, amount range, payment status)."""
    return payment_controller.get_payments(
        db,
        event_title,
        buyer_email,
        organizer_email,
        amount_min,
        amount_max,
        fee_min,
        fee_max,
        brut_amount_min,
        brut_amount_max,
        stripe_session_id,
        stripe_payment_intent_id,
        status,
        date_apres,
        date_avant,
        offset,
        limit
    )


# 🔹 7. Récupérer les types
@router.get("/types", response_model=TypeListSchemaResponse, status_code=200)
def get_types(
    _: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
) -> TypeListSchemaResponse:
    """Retrieve a list of all types (e.g., event types)."""
    return type_controller.get_types(db)
