"""This file contains the role enum"""
from enum import Enum

class RoleEnum(str, Enum):
    """used to work with role objects"""
    ROLE_USER = "ROLE_USER"
    ROLE_ADMIN = "ROLE_ADMIN"
    ROLE_SUPER_ADMIN = "ROLE_SUPER_ADMIN"
