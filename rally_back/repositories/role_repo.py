"""This file contains the role repository"""
from sqlalchemy.orm import Session
from enums.role import RoleEnum
from models.role_model import Role

def add_role(db: Session, role: Role)->None:
    """used to add a role in db"""
    db.add(role)

def commit_role(db: Session)->None:
    """used to commit changes in db"""
    db.commit()

def refresh_role(db: Session, role: Role)->None:
    """used to refresh a role"""
    db.refresh(role)

def get_role_by_role_enum(db: Session, role: RoleEnum)->Role:
    """used to fetch a role according by an enum value"""
    return db.query(Role).filter(Role.role == role).first()

def get_role_by_id(db: Session, role_id: int)->Role:
    """used to fetch a role by its id"""
    return db.query(Role).filter(Role.id == role_id).first()
