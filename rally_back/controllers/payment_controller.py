"""
This file contains the controller related to payments
"""
import os
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
import stripe
from services import event_service, payment_service, profile_service, registration_service, user_service
from models.user_model import User
from enums.payment_status import PaymentStatusEnum
from schemas.response_schemas.payment_schema_response import (
    PaymentSchemaResponse,
    PaymentListSchemaResponse,
    PaymentRestrictedSchemaResponse,
    PaymentRestrictedListSchemaResponse
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_check_out_session(db: Session, event_id: int, current_user: User)->dict[str, str]:
    """
    Creates a checkout session for a user to pay for event registration.

    This function checks if the event exists, verifies if the user is eligible to register (not already registered),
    and processes payment via a checkout session if the event has a price. It also handles the registration process
    and assigns a commission fee for the organizer.

    Args:
        db (Session): The database session to interact with the database.
        event_id (int): The ID of the event the user wants to register for.
        current_user (User): The current user attempting to register for the event.

    Returns:
        dict[str, str]: A dictionary containing a session URL for the checkout process or a confirmation message if registration is free.

    Raises:
        HTTPException:
            - If the event is not found.
            - If the user is not found or does not have an account ID.
            - If the user is already registered for the event.
            - If there is an error during the checkout session creation.
    """
    event = event_service.get_event_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    profile = profile_service.get_profile(db, event.profile_id)
    user = user_service.get_user(db, profile.user_id)

    if not event:
        raise HTTPException(status_code=404, detail="Event not found")

    if not user or not user.account_id:
        raise HTTPException(status_code=404, detail="User not found")

    registration = registration_service.get_registration(db, current_user.id, event.id)
    if registration:
        raise HTTPException(status_code=403, detail="User deja inscrit pour cet event")
    registration = registration_service.register_for_event(db, current_user.id, event_id)

    try:
        if event.price > 0:
            commission_fee = int((event.price * 0.05) * 100)
            amount = int(event.price * 100)

            metadata = {
                "buyer_id": str(current_user.id),
                "organizer_id": str(event.profile_id),
                "event_id": str(event.id),
                "brut_amount": str(event.price),
                "fee": str(commission_fee),
                "registration_id": str(registration.id)
            }

            checkcout_session = payment_service.create_checkout_session(amount, event.title, event.id, commission_fee, metadata, user.account_id)
            payment_service.create_payment(
                db,
                event.id,
                current_user.id,
                user.id,
                (event.price * 0.95),
                (event.price * 0.05),
                event.price,
                checkcout_session.id,
                checkcout_session.payment_intent
            )
            return {"session_url": checkcout_session.url}
        registration_service.update_registration_status(db, PaymentStatusEnum.FREE, registration.id)
        return {"registration": "ok"}
    except Exception as e:
        registration_service.delete_registration(db, current_user.id, event.id)
        raise HTTPException(status_code=500, detail=f"Error creating checkout session: {str(e)}") from e

def get_onboarding_url(db: Session, current_user: User)->dict[str, str]:
    """
    Creates an onboarding URL for a user to complete their Stripe account setup.

    This function creates a Stripe Connect account for the user (if not already created),
    updates the user's account ID in the database, and generates an onboarding URL to
    allow the user to finish setting up their Stripe account.

    Args:
        db (Session): The database session to interact with the database.
        current_user (User): The current user who needs to complete their Stripe onboarding.

    Returns:
        dict[str, str]: A dictionary containing the generated onboarding URL for the user.

    Raises:
        HTTPException: If an error occurs during the creation of the Stripe account or generation of the onboarding URL.
    """
    account = payment_service.create_connect_account(current_user.email)
    onboarding_url = payment_service.create_account_onboarding_link(account["id"])
    # user_service.update_stripe_account(db, current_user.id, account["id"])
    return {"onboarding_url": onboarding_url}

def handle_webhooks(event: dict, db: Session):
    """
    Handles incoming Stripe webhook events and processes them.

    This function receives a webhook event from Stripe, processes it using the
    `payment_service.handle_stripe_webhook_event` method, and updates the database
    accordingly based on the event type.

    Args:
        event (dict): The webhook event data sent by Stripe.
        db (Session): The database session to interact with the database.

    Returns:
        The result of processing the webhook event through the `payment_service.handle_stripe_webhook_event` method.
    """
    return payment_service.handle_stripe_webhook_event(event, db)

def get_payments(
    db: Session,
    event_title: Optional[str],
    buyer_email: Optional[str],
    organizer_email: Optional[str],
    amount_min: Optional[float],
    amount_max: Optional[float],
    fee_min: Optional[float],
    fee_max: Optional[float],
    brut_amount_min: Optional[float],
    brut_amount_max: Optional[float],
    stripe_session_id: Optional[str],
    stripe_payment_intent_id: Optional[str],
    status: Optional[PaymentStatusEnum],
    date_apres: Optional[datetime],
    date_avant: Optional[datetime],
    offset: int,
    limit: int
) -> PaymentListSchemaResponse:
    """
    Retrieves a list of payments based on various filters and pagination parameters.

    This function queries the payments from the database based on the provided filters such as event title,
    buyer and organizer emails, amount ranges, payment status, and date ranges. It also supports pagination
    through the offset and limit parameters.

    Args:
        db (Session): The database session to interact with the database.
        event_title (Optional[str]): Filter payments by event title.
        buyer_email (Optional[str]): Filter payments by buyer's email.
        organizer_email (Optional[str]): Filter payments by organizer's email.
        amount_min (Optional[float]): Filter payments by minimum amount.
        amount_max (Optional[float]): Filter payments by maximum amount.
        fee_min (Optional[float]): Filter payments by minimum fee.
        fee_max (Optional[float]): Filter payments by maximum fee.
        brut_amount_min (Optional[float]): Filter payments by minimum brut amount.
        brut_amount_max (Optional[float]): Filter payments by maximum brut amount.
        stripe_session_id (Optional[str]): Filter payments by Stripe session ID.
        stripe_payment_intent_id (Optional[str]): Filter payments by Stripe payment intent ID.
        status (Optional[PaymentStatusEnum]): Filter payments by payment status.
        date_apres (Optional[datetime]): Filter payments after this date.
        date_avant (Optional[datetime]): Filter payments before this date.
        offset (int): The offset for pagination (skip this number of records).
        limit (int): The number of records to retrieve (pagination limit).

    Returns:
        PaymentListSchemaResponse: The list of payments matching the filter criteria along with pagination info.

    Raises:
        HTTPException: If there is an issue with the database query or any other error.
    """
    payments = payment_service.get_payments(
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

    all_payments = []

    for payment in payments:
        all_payments.append(
            PaymentSchemaResponse(
                id=payment.id,
                event_id=payment.event_id,
                event_title=payment.event_title,
                buyer_id=payment.buyer_id,
                buyer_email=payment.buyer_email,
                organizer_id=payment.organizer_id,
                organizer_email=payment.organizer_email,
                amount=payment.amount,
                fee=payment.fee,
                brut_amount=payment.brut_amount,
                stripe_session_id=payment.stripe_session_id,
                stripe_payment_intent_id=payment.stripe_payment_intent_id,
                status=payment.status,
                created_at=payment.created_at
            )
        )

    total = payment_service.get_payments_total_count(
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
        date_avant
    )

    return PaymentListSchemaResponse(count=len(all_payments), data=all_payments, total=total)


def get_payments_for_user(
    db: Session,
    current_user: User,
    event_title: Optional[str],
    organizer_email: Optional[str],
    brut_amount_min: Optional[float],
    brut_amount_max: Optional[float],
    status: Optional[PaymentStatusEnum],
    date_apres: Optional[datetime],
    date_avant: Optional[datetime],
    offset: int,
    limit: int
) -> PaymentRestrictedListSchemaResponse:
    """
    Retrieves a list of payments for the current user based on various filters and pagination parameters.

    This function queries the payments made by the current user, applying filters such as event title,
    organizer email, brut amount ranges, payment status, and date ranges. Pagination is also supported
    through the offset and limit parameters.

    Args:
        db (Session): The database session to interact with the database.
        current_user (User): The current authenticated user.
        event_title (Optional[str]): Filter payments by event title.
        organizer_email (Optional[str]): Filter payments by organizer's email.
        brut_amount_min (Optional[float]): Filter payments by minimum brut amount.
        brut_amount_max (Optional[float]): Filter payments by maximum brut amount.
        status (Optional[PaymentStatusEnum]): Filter payments by payment status.
        date_apres (Optional[datetime]): Filter payments after this date.
        date_avant (Optional[datetime]): Filter payments before this date.
        offset (int): The offset for pagination (skip this number of records).
        limit (int): The number of records to retrieve (pagination limit).

    Returns:
        PaymentRestrictedListSchemaResponse: A list of payments matching the filter criteria along with pagination info.

    Raises:
        HTTPException: If there is an issue with the database query or any other error.
    """
    payments = payment_service.get_payments_by_user_id(
        db,
        current_user.id,
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

    all_payments = []

    for payment in payments:
        all_payments.append(
            PaymentRestrictedSchemaResponse(
                id=payment.id,
                event_id=payment.event_id,
                event_title=payment.event_title,
                buyer_id=payment.buyer_id,
                buyer_email=payment.buyer_email,
                organizer_id=payment.organizer_id,
                organizer_email=payment.organizer_email,
                brut_amount=payment.brut_amount,
                status=payment.status,
                created_at=payment.created_at
            )
        )

    return PaymentRestrictedListSchemaResponse(count=len(all_payments), data=all_payments)
