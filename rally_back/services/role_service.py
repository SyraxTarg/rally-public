from sqlalchemy.orm import Session

from enums.role import RoleEnum
from models.role_model import Role
from repositories import role_repo



def create_role_user(db: Session)->Role:
    """used to create a role user"""
    role_user = Role(role=RoleEnum.ROLE_USER)
    role_repo.add_role(db, role_user)
    role_repo.commit_role(db)
    role_repo.refresh_role(db, role_user)
    return role_user

def create_role_admin(db: Session)->Role:
    """used to create a role admin"""
    role_admin = Role(role=RoleEnum.ROLE_ADMIN)
    role_repo.add_role(db, role_admin)
    role_repo.commit_role(db)
    role_repo.refresh_role(db, role_admin)
    return role_admin

def create_role_super_admin(db: Session)->Role:
    """used to create a role super-admin"""
    role_super_admin = Role(role=RoleEnum.ROLE_SUPER_ADMIN)
    role_repo.add_role(db, role_super_admin)
    role_repo.commit_role(db)
    role_repo.refresh_role(db, role_super_admin)
    return role_super_admin

def get_role_user(db: Session)->Role:
    """used to fetch the role_user"""
    return role_repo.get_role_by_role_enum(db, RoleEnum.ROLE_USER)

def get_role_admin(db: Session)->Role:
    """used to fetch the role admin"""
    return role_repo.get_role_by_role_enum(db, RoleEnum.ROLE_ADMIN)

def get_role_super_admin(db: Session)->Role:
    """used to fetch the role super-admin"""
    return role_repo.get_role_by_role_enum(db, RoleEnum.ROLE_SUPER_ADMIN)

def get_role(db: Session, role: RoleEnum)->Role:
    """used to get role by role enum"""
    return role_repo.get_role_by_role_enum(db, role)

def get_role_by_id(db: Session, role_id: int)->Role:
    """used to get role by its id"""
    return role_repo.get_role_by_id(db, role_id)
