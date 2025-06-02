"""This file contains the failed login repository"""
from sqlalchemy.orm import Session
from models.failed_login_model import FailedLogin


def get_failed_login_by_ip_address(db: Session, client_ip: int)->FailedLogin:
    """
    This function is used to fetch a failed login according to its client ip.
    """
    return db.query(FailedLogin).filter(FailedLogin.ip_address == client_ip).first()

def add_new_failed_login(db: Session, failed_login: FailedLogin)->None:
    """
    This function is used to add a new failed login in the database.
    """
    db.add(failed_login)

def commit_failed_login(db: Session)->None:
    """
    This function is used to commit the changes in the database.
    """
    db.commit()

def refresh_failed_login(db: Session, failed_login: FailedLogin)->None:
    """
    This function is used to refresh an object in the database.
    """
    db.refresh(failed_login)

def delete_failed_login(db: Session, failed_login: FailedLogin)->None:
    """
    This function is used to delete a failed login in the database.
    """
    db.delete(failed_login)
