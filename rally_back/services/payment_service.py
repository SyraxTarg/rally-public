from typing import Optional
import os
from datetime import datetime
import stripe
from fastapi import status
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader


from enums.payment_status import PaymentStatusEnum
from models.payment_model import Payment
from services import event_service, registration_service, user_service, email_service
from repositories import payment_repo
from errors import (
    PaymentError,
    CheckoutError,
    StripeAccountError,
    UserNotFoundError,
    EventNotFound,
    PaymentNotFound,
    RegistrationNotFound,
)



load_dotenv()

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def create_checkout_session(amount: int, event: str, event_id: int, app_fee: int = 0, metadata: dict = {}, connected_account_id: str = None):
    """used to create a stripe session and a link leading to a payment page"""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{
                "price_data": {
                    "currency": "eur",
                    "product_data": {
                        "name": event,
                    },
                    "unit_amount": amount,
                },
                "quantity": 1,
            }],
            mode="payment",
            success_url=f"{os.getenv('STRIPE_SUCCESS_URL')}/{event_id}?onboarding=success",
            cancel_url=f"{os.getenv('STRIPE_CANCEL_URL')}/{event_id}?onboarding=error",
            metadata=metadata,
            payment_intent_data={
                "transfer_data": {
                    "destination": connected_account_id,
                },
                "application_fee_amount": app_fee,
                "metadata": metadata
            }
        )
        return session
    except Exception as e:
        raise CheckoutError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error during checkout"
        ) from e


def create_connect_account(email: str) -> dict:
    """used to create a stripe connected account"""
    try:
        return stripe.Account.create(
            type="express",
            country="FR",
            email=email,
            capabilities={
                "transfers": {"requested": True},
                "card_payments": {"requested": True}
            }
        )
    except Exception as e:
        raise StripeAccountError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error during account creation"
        ) from e


def create_account_onboarding_link(account_id: str) -> str:
    """used to generate a link leading to page where the user can finalize their account creation"""
    try:
        link = stripe.AccountLink.create(
            account=account_id,
            refresh_url=f"{os.getenv('STRIPE_REFRESH_URL')}?account=error",
            return_url=f"{os.getenv('STRIPE_RETURN_URL')}?account=success",
            type="account_onboarding"
        )
        return link.url
    except Exception as e:
        raise PaymentError(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error during payment"
        ) from e


def create_payment(
    db: Session,
    event_id: int,
    buyer_id: int,
    organizer_id: int,
    amount: float,
    fee: float,
    brut_amount: float,
    stripe_session_id: str,
    payment_intent: str
) -> Payment:
    """used to create a new payment instance in db"""
    buyer = user_service.get_user(db, buyer_id)
    if not buyer:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    organizer = user_service.get_user(db, organizer_id)
    if not organizer:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    event = event_service.get_event_by_id(db, event_id)
    if not event:
        raise EventNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event not found"
        )

    new_payment = Payment(
        event_id=event_id,
        event_title= event.title,
        buyer_id=buyer_id,
        buyer_email=buyer.email,
        organizer_id=organizer_id,
        organizer_email=organizer.email,
        amount=amount,
        fee=fee,
        brut_amount=brut_amount,
        stripe_session_id=stripe_session_id,
        stripe_payment_intent_id=payment_intent,
        status=PaymentStatusEnum.PENDING,
        created_at=datetime.now()
    )

    payment_repo.add_payment(db, new_payment)
    payment_repo.commit_payment(db)
    payment_repo.refresh_payment(db, new_payment)
    return new_payment


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
    payment_status: Optional[PaymentStatusEnum],
    date_apres: Optional[datetime],
    date_avant: Optional[datetime],
    offset: int,
    limit: int
) -> list[Payment]:
    """used to get all payments from db according to given filters"""
    return payment_repo.get_payment_filters(
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
        payment_status,
        date_apres,
        date_avant,
        offset,
        limit
    )
    
    
def get_payments_total_count(
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
    payment_status: Optional[PaymentStatusEnum],
    date_apres: Optional[datetime],
    date_avant: Optional[datetime],
) -> list[Payment]:
    """used to get all payments from db according to given filters"""
    return payment_repo.get_payment_filters_total_count(
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
        payment_status,
        date_apres,
        date_avant,
    )


def get_payment_by_id(db: Session, payment_id: int) -> Payment:
    """used to fetch a payment from db by its id"""
    payment = payment_repo.get_payment_by_id(db, payment_id)
    if not payment:
        raise PaymentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment


def change_payment_status(db: Session, payment_status: PaymentStatusEnum, payment_id: int, intent_id: str) -> Payment:
    """used to change the payment status"""
    payment = get_payment_by_id(db, payment_id)
    if not payment:
        raise PaymentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    payment.status = payment_status
    payment.stripe_payment_intent_id = intent_id

    payment_repo.commit_payment(db)
    payment_repo.refresh_payment(db, payment)
    return payment


def handle_stripe_webhook_event(event: dict, db: Session):
    """used by stripe as a webhook when a payment is made"""
    event_type = event.get("type")
    data = event["data"]["object"]
    
    if event_type == "account.updated":
        if data.get("details_submitted") and data.get("email"):
            user = user_service.get_user_by_email(db, data["email"])
            if user:
                user_service.update_stripe_account(db, user.id, data["id"])
            return

    metadata = data.get("metadata", {})
    session_id = data.get("id")
    intent_id = data.get("payment_intent")

    if not session_id and metadata:
        return

    existing_payment = get_payment_by_session_id(db, session_id)
    if not existing_payment:
        raise PaymentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    payment_status = None
    if event_type == "checkout.session.completed":
        payment_status = PaymentStatusEnum.SUCCESS
    elif event_type == "checkout.session.async_payment_failed":
        payment_status = PaymentStatusEnum.FAILED
    elif event_type == "checkout.session.async_payment_pending":
        payment_status = PaymentStatusEnum.PENDING
    elif event_type == "checkout.session.expired":
        payment_status = PaymentStatusEnum.FAILED
    else:
        return

    registration_id = int(metadata["registration_id"])
    if not registration_id:
        raise RegistrationNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Missing registration_id in metadata"
        )

    change_payment_status(db, payment_status, existing_payment.id, intent_id)
    if status == PaymentStatusEnum.FAILED:
        registration_service.delete_registration_by_id(db, registration_id)
    else:
        registration_service.update_registration_status(db, payment_status, registration_id)
        send_facture(db, existing_payment.id)


def get_payment_by_event_and_users(db: Session, event_id: int, buyer_id: int, organizer_id: int) -> Payment:
    """used to get a payment by its event and user"""
    payment = payment_repo.get_payment_by_event_and_users(db, event_id, buyer_id, organizer_id)
    if not payment:
        raise PaymentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment

def get_payment_by_session_id(db: Session, session_id: str) -> Payment:
    """used to get a payment by its session id"""
    payment = payment_repo.get_payment_by_session_id(db, session_id)
    if not payment:
        raise PaymentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    return payment

def get_payments_by_user_id(
    db: Session,
    user_id: int,
    event_title: Optional[str],
    organizer_email: Optional[str],
    brut_amount_min: Optional[float],
    brut_amount_max: Optional[float],
    payment_status: Optional[PaymentStatusEnum],
    date_apres: Optional[datetime],
    date_avant: Optional[datetime],
    offset: int,
    limit: int
) -> list[Payment]:
    """used to get payments by user id and given filters"""
    return payment_repo.get_payments_by_user_id_filters(
        db,
        user_id,
        event_title,
        organizer_email,
        brut_amount_min,
        brut_amount_max,
        payment_status,
        date_apres,
        date_avant,
        offset,
        limit
    )

def send_facture(db: Session, payment_id: int)-> bool:
    """used to send factures by email"""
    payment = payment_repo.get_payment_by_id(db, payment_id)
    if not payment:
        raise PaymentNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )

    buyer = user_service.get_user_by_email(db, payment.buyer_email)
    if not buyer:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    organizer = user_service.get_user_by_email(db, payment.organizer_email)
    if not organizer:
        raise UserNotFoundError(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    env = Environment(loader=FileSystemLoader("templates"))

    template_facture = env.get_template("facture.html")
    facture_content = template_facture.render(
        payment=payment
    )
    email_service.send_email(facture_content, buyer.email, f"Facture de votre paiement pour {payment.event_title}")

    template_recu = env.get_template("recu_organizer.html")
    recu_content = template_recu.render(
        payment=payment
    )
    email_service.send_email(recu_content, organizer.email, f"Reçu de paiement pour {payment.event_title}")

    return True
