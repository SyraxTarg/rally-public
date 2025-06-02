from sqlalchemy.orm import Session
from fastapi import status

from models.reason_model import Reason
from repositories import reason_repo
from errors import ReasonAlreadyExists, ReasonNotFound




def create_reason(db: Session, reason: str)->Reason:
    """used to create a new reason"""
    existing_reason = reason_repo.get_reason_by_reason(db, reason)
    if existing_reason:
        raise ReasonAlreadyExists(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"La raison '{reason}' existe déjà."
        )
    new_reason = Reason(reason=reason)
    reason_repo.add_reason(db, new_reason)
    reason_repo.commit_reason(db)
    reason_repo.refresh_reason(db, new_reason)
    return new_reason

def get_reasons(db: Session)->list[Reason]:
    """used to fetch all reasons"""
    return reason_repo.get_all_reasons(db)

def get_reason_by_id(db: Session, reason_id: int)->Reason:
    """used to get a reason by its id"""
    reason = reason_repo.get_reason_by_id(db, reason_id)
    if not reason:
        raise ReasonNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reason not found"
        )
    return reason

def delete_reason(db: Session, reason_id: int)->None:
    """used to delete a reason"""
    reason = get_reason_by_id(db, reason_id)

    if reason:
        raise ReasonNotFound(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Reason not found"
        )

    reason_repo.delete_reason(db, reason)
    reason_repo.commit_reason(db)
