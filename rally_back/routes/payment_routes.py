import os
from datetime import datetime
from fastapi import Depends, APIRouter, Query, Request, HTTPException, Header
from sqlalchemy.orm import Session
import stripe

from controllers import authent_controller, payment_controller
from database.db import get_db
from models.user_model import User
from enums.payment_status import PaymentStatusEnum
from schemas.response_schemas.payment_schema_response import PaymentRestrictedListSchemaResponse

router = APIRouter(
    prefix="/api/v1/payments",
    tags=["payments"],
)

@router.post("/checkout")
def create_session_endpoint(
    event_id: int = Query,
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
)->dict[str, str]:
    """Create a Stripe checkout session for a user to complete their payment for an event."""
    return payment_controller.create_check_out_session(db, event_id, current_user)

@router.post("/create-account")
def create_account(
    current_user: User = Depends(authent_controller.get_connected_user),
    db: Session = Depends(get_db)
):
    """Create a Stripe account for the user and return the onboarding URL."""
    return payment_controller.get_onboarding_url(db, current_user)

@router.post("/webhook/stripe")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: Session = Depends(get_db)
):
    """Handle Stripe webhook events for payment status updates."""
    payload = await request.body()
    endpoint_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=stripe_signature,
            secret=endpoint_secret
        )
    except HTTPException as e:
        raise HTTPException(status_code=400, detail="Signature invalide") from e

    payment_controller.handle_webhooks(event, db)

    return {"status": "ok"}

@router.get("/", response_model=PaymentRestrictedListSchemaResponse)
def get_payments_for_current_user(
    event_title: str = Query(None),
    organizer_email: str = Query(None),
    brut_amount_min: float = Query(None),
    brut_amount_max: float = Query(None),
    status: PaymentStatusEnum = Query(None),
    date_apres: datetime = Query(None),
    date_avant: datetime = Query(None),
    current_user: User = Depends(authent_controller.get_connected_user),
    offset: int = Query(0),
    limit: int = Query(5),
    db: Session = Depends(get_db)
)->PaymentRestrictedListSchemaResponse:
    """Get a paginated list of payments made by the current user with optional filters."""
    return payment_controller.get_payments_for_user(
        db,
        current_user,
        event_title,
        organizer_email,
        brut_amount_min,
        brut_amount_max,
        status,
        date_apres,
        date_avant,
        offset,
        limit
    )
