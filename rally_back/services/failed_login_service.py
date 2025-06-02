from datetime import datetime
from sqlalchemy.orm import Session
from models.failed_login_model import FailedLogin
from repositories import failed_login_repo




def get_failed_login(db: Session, client_ip: int)->FailedLogin:
    """used to fetch a failed login by its client id"""
    return failed_login_repo.get_failed_login_by_ip_address(db, client_ip)


def create_failed_login(db: Session, client_ip: int)->FailedLogin:
    """used to create a new failed login instance"""
    failed_login = FailedLogin(ip_address=client_ip, attempts=1, last_attempt=datetime.now())
    failed_login_repo.add_new_failed_login(db, failed_login)
    failed_login_repo.commit_failed_login(db)
    failed_login_repo.refresh_failed_login(db, failed_login)


def update_failed_login(db: Session, failed_login: FailedLogin)->FailedLogin:
    """used to update a failed login instance"""
    failed_login.attempts += 1
    failed_login.last_attempt = datetime.now()
    failed_login_repo.commit_failed_login(db)


def delete_failed_login(db: Session, failed_login: FailedLogin)->None:
    """used to delete a failed login instance"""
    failed_login_repo.delete_failed_login(db, failed_login)
    failed_login_repo.commit_failed_login(db)


def reset_failed_login(db: Session, failed_login: FailedLogin)->None:
    """used to reset a failed login instance to attempts zero"""
    failed_login.attempts = 0
    failed_login_repo.commit_failed_login(db)
