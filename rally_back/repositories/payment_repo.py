"""This file contains the payment repository"""
from typing import Optional
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import func
from enums.payment_status import PaymentStatusEnum
from models.payment_model import Payment

def add_payment(db: Session, payment: Payment)->None:
    """
    This function is used to add a new payment in db.
    """
    db.add(payment)

def commit_payment(db: Session)->None:
    """
    This function is used to commit changes from db.
    """
    db.commit()

def refresh_payment(db: Session, payment: Payment)->None:
    """
    This function is used to refresh a payment.
    """
    db.refresh(payment)

def get_payment_filters(
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
)->list[Payment]:
    """
    This function is used to fetch all the payments from db according to given filters.
    """
    query = db.query(Payment)

    if date_avant is not None:
        query = query.filter(func.date(Payment.created_at) <= date_avant.date())

    if date_apres is not None:
        query = query.filter(func.date(Payment.created_at) >= date_apres.date())

    if event_title is not None:
        query = query.filter(Payment.event_title.ilike(f"%{event_title}%"))

    if buyer_email is not None:
        query = query.filter(Payment.buyer_email == buyer_email)

    if organizer_email is not None:
        query = query.filter(Payment.organizer_email == organizer_email)

    if amount_min is not None:
        query = query.filter(Payment.amount >= amount_min)

    if amount_max is not None:
        query = query.filter(Payment.amount <= amount_max)

    if fee_min is not None:
        query = query.filter(Payment.fee >= fee_min)

    if fee_max is not None:
        query = query.filter(Payment.fee <= fee_max)

    if brut_amount_min is not None:
        query = query.filter(Payment.brut_amount >= brut_amount_min)

    if brut_amount_max is not None:
        query = query.filter(Payment.brut_amount <= brut_amount_max)

    if stripe_session_id is not None:
        query = query.filter(Payment.stripe_session_id == stripe_session_id)

    if stripe_payment_intent_id is not None:
        query = query.filter(Payment.stripe_payment_intent_id == stripe_payment_intent_id)

    if status is not None:
        query = query.filter(Payment.status == status)

    return query.order_by(Payment.created_at.desc()).offset(offset).limit(limit).all()

def get_payment_by_id(db: Session, payment_id: int)->Payment:
    """
    This function is used to fetch a payment from db according to its id.
    """
    return db.query(Payment).filter(Payment.id == payment_id).first()

def get_payments_by_user_id_filters(
    db: Session,
    user_id: int,
    event_title: Optional[str],
    organizer_email: Optional[str],
    brut_amount_min: Optional[float],
    brut_amount_max: Optional[float],
    status: Optional[PaymentStatusEnum],
    date_apres: Optional[datetime],
    date_avant: Optional[datetime],
    offset: int,
    limit: int
)->list[Payment]:
    """
    This function is used to fetch payments from db according to a user and given filters.
    """
    query = db.query(Payment).filter(Payment.buyer_id == user_id)

    if date_avant is not None:
        query = query.filter(func.date(Payment.created_at) <= date_avant.date())

    if date_apres is not None:
        query = query.filter(func.date(Payment.created_at) >= date_apres.date())

    if event_title is not None:
        query = query.filter(Payment.event_title.ilike(f"%{event_title}%"))

    if organizer_email is not None:
        query = query.filter(Payment.organizer_email == organizer_email)

    if brut_amount_min is not None:
        query = query.filter(Payment.brut_amount >= brut_amount_min)

    if brut_amount_max is not None:
        query = query.filter(Payment.brut_amount <= brut_amount_max)

    if status is not None:
        query = query.filter(Payment.status == status)

    return query.order_by(Payment.created_at.desc()).offset(offset).limit(limit).all()

def get_payment_by_event_and_users(db: Session, event_id: int, buyer_id: int, organizer_id: int)->Payment:
    """
    This function is used to fetch a payment according to its event and users.
    """
    return db.query(Payment).filter(Payment.event_id == event_id).filter(Payment.buyer_id == buyer_id).filter(Payment.organizer_id == organizer_id).first()

def get_payment_by_session_id(db: Session, session_id: str)->Payment:
    """
    This function is used to fet a payment by its session id.
    """
    return db.query(Payment).filter(Payment.stripe_session_id==session_id).first()


def get_payment_filters_total_count(
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
)->int:
    """
    This function is used to fetch all the payments from db according to given filters.
    """
    query = db.query(Payment)

    if date_avant is not None:
        query = query.filter(func.date(Payment.created_at) <= date_avant.date())

    if date_apres is not None:
        query = query.filter(func.date(Payment.created_at) >= date_apres.date())

    if event_title is not None:
        query = query.filter(Payment.event_title.ilike(f"%{event_title}%"))

    if buyer_email is not None:
        query = query.filter(Payment.buyer_email == buyer_email)

    if organizer_email is not None:
        query = query.filter(Payment.organizer_email == organizer_email)

    if amount_min is not None:
        query = query.filter(Payment.amount >= amount_min)

    if amount_max is not None:
        query = query.filter(Payment.amount <= amount_max)

    if fee_min is not None:
        query = query.filter(Payment.fee >= fee_min)

    if fee_max is not None:
        query = query.filter(Payment.fee <= fee_max)

    if brut_amount_min is not None:
        query = query.filter(Payment.brut_amount >= brut_amount_min)

    if brut_amount_max is not None:
        query = query.filter(Payment.brut_amount <= brut_amount_max)

    if stripe_session_id is not None:
        query = query.filter(Payment.stripe_session_id == stripe_session_id)

    if stripe_payment_intent_id is not None:
        query = query.filter(Payment.stripe_payment_intent_id == stripe_payment_intent_id)

    if status is not None:
        query = query.filter(Payment.status == status)

    return query.order_by(Payment.created_at.desc()).count()
